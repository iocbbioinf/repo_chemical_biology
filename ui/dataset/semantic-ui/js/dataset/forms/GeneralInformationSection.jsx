import React from "react";
import _get from "lodash/get";
import { buildUID } from "react-searchkit";
import Overridable from "react-overridable";
import { Header } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { CCMMSections } from "@js/ccmm_invenio/forms";
import { EDTFSingleDatePicker, TextField } from "@js/oarepo_ui/forms";
import {
  ResourceTypeField,
  PublisherField,
  VersionField,
  SubjectsField,
} from "@js/invenio_rdm_records";
import { PIDFieldList } from "@js/oarepo_rdm/form/components";
import { TextAreaField } from "./fields";
import { LocationsField } from "./LocationsField";
import { PersonFields } from "./PersonFields";
import { SampleSection } from "./SampleSection";

const ccmmSection = (key) => CCMMSections.find((section) => section.key === key);

export const CCMMFiles = ccmmSection("files");
export const CCMMCommunityAndAccess = ccmmSection("community-and-access");

/**
 * General information tab. Based on the CCMM general information, but with one
 * title, one plain text description, two persons (PI = creator, sample preparer =
 * contributor with role Data Collector) and one geolocation, without languages,
 * licenses and dates. Followed by the sample and analysis metadata.
 */
export const GeneralInformationSection = {
  key: "general-information",
  label: i18next.t("General information"),
  component: (tabConfig) => {
    const { record, formConfig } = tabConfig;
    const { vocabularies, pids, is_doi_required: isDoiRequired } = formConfig.config;
    const { overridableIdPrefix } = formConfig;
    return (
      <>
        <Overridable id={buildUID(overridableIdPrefix, "PIDField")} {...tabConfig}>
          <PIDFieldList pids={pids} record={record} isDoiRequired={isDoiRequired} />
        </Overridable>
        <TextField fieldPath="metadata.title" label={i18next.t("Title")} required />
        <TextAreaField
          fieldPath="metadata.description"
          label={i18next.t("Abstract / description")}
          rows={6}
        />
        <ResourceTypeField
          options={vocabularies?.resource_type}
          fieldPath="metadata.resource_type"
          required
        />
        <EDTFSingleDatePicker fieldPath="metadata.publication_date" />
        <PublisherField fieldPath="metadata.publisher" required={isDoiRequired} />
        <VersionField fieldPath="metadata.version" />
        <SubjectsField
          fieldPath="metadata.subjects"
          initialOptions={_get(record, "ui.subjects", null)}
          limitToOptions={vocabularies?.subjects?.limit_to}
          searchOnFocus
        />
        <LocationsField />

        <Header as="h2" size="medium" dividing className="rel-mt-2">
          {i18next.t("Persons")}
        </Header>
        <PersonFields
          title={i18next.t("PI")}
          personPath="metadata.creators.0"
          emailPath="metadata.principal_investigator_email"
          countryPath="metadata.principal_investigator_country"
          required
        />
        <PersonFields
          title={i18next.t("Sample prepared by")}
          personPath="metadata.contributors.0"
          emailPath="metadata.sample_preparer_email"
          countryPath="metadata.sample_preparer_country"
        />

        <Header as="h2" size="medium" dividing className="rel-mt-2">
          {SampleSection.label}
        </Header>
        <SampleSection.component {...tabConfig} />
      </>
    );
  },
  includesPaths: [
    "pids",
    "metadata.title",
    "metadata.description",
    "metadata.resource_type",
    "metadata.publication_date",
    "metadata.publisher",
    "metadata.version",
    "metadata.subjects",
    "metadata.locations",
    "metadata.creators",
    "metadata.contributors",
    "metadata.principal_investigator_email",
    "metadata.principal_investigator_country",
    "metadata.sample_preparer_email",
    "metadata.sample_preparer_country",
    ...SampleSection.includesPaths,
  ],
};
