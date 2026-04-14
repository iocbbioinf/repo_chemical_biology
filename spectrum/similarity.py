"""Similarity (kNN vector) search for spectrum records."""

from flask import g
from flask_resources import resource_requestctx, response_handler, route
from invenio_records_resources.resources.records.resource import (
    request_data,
    request_extra_args,
)
from invenio_search import current_search_client


class SimilaritySearchResourceMixin:
    """Adds POST /api/spectrum/records/search-similar endpoint."""

    def create_url_rules(self):
        rules = super().create_url_rules()
        rules.append(route("POST", "/spectrum/records/search-similar", self.search_similar))
        return rules

    @request_extra_args
    @request_data
    @response_handler(many=True)
    def search_similar(self):
        """Search for records whose embedding is closest to the provided vector.

        Request body::

            {
                "vector": [0.1, 0.9],
                "k": 10
            }

        Returns the k nearest neighbours sorted by score.
        """
        identity = g.identity
        body = resource_requestctx.data or {}
        vector = body.get("vector")
        k = int(body.get("k", 10))

        if not vector or not isinstance(vector, list):
            from flask import abort
            abort(400, "Request body must contain a 'vector' list.")

        hits = self.service.search_similar(
            identity=identity,
            vector=vector,
            k=k,
            params=resource_requestctx.args,
            expand=resource_requestctx.args.get("expand", False),
        )
        return hits.to_dict(), 200


class SimilaritySearchServiceMixin:
    """Adds search_similar() to the record service."""

    def search_similar(self, identity, vector, k=10, params=None, expand=False):
        """Return the k records whose embedding is nearest to *vector*.

        Uses OpenSearch kNN query on the ``metadata.embedding`` field.
        Bypasses opensearch-dsl (which doesn't know the knn query type) and
        executes a raw request via current_search_client.
        """
        self.require_permission(identity, "search")

        params = params or {}

        # Build a base search to get the correct index name and permission filters.
        search = self.search_request(
            identity,
            params,
            self.record_cls,
            self.config.search,
            permission_action="read",
        )

        # Extract the index name(s) from the DSL search object.
        index = ",".join(search._index) if search._index else "_all"

        # Extract any permission/filter query already set on the search object
        # (e.g. visibility filters) so we can AND it with the kNN query.
        existing = search.to_dict()
        existing_filter = existing.get("query")

        knn_clause = {
            "metadata.embedding": {
                "vector": vector,
                "k": k,
            }
        }

        if existing_filter:
            query_body = {
                "query": {
                    "bool": {
                        "must": [{"knn": knn_clause}],
                        "filter": existing_filter,
                    }
                }
            }
        else:
            query_body = {"query": {"knn": knn_clause}}

        query_body["size"] = k

        raw_response = current_search_client.search(
            index=index,
            body=query_body,
        )

        # Wrap raw response in the same AttrDict opensearch-dsl would produce
        # so that result_list() can iterate hits normally.
        from opensearch_dsl.response import Response
        search_result = Response(search, raw_response)

        return self.result_list(
            self,
            identity,
            search_result,
            params,
            links_item_tpl=self.links_item_tpl,
            expand=expand,
        )
