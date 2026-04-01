# Repository for Chemical Biology Data

**The mass spectra repository will be a platform that enables similarity-based spectrum searches using various algorithms. The handling of data and metadata will be built on FAIR principles.**

This codebase was created following [this tutorial](https://nrp-cz.github.io/docs/installation/create_instance).

Destination repo: https://github.com/iocbbioinf/repo_chemical_biology

## ./run.sh upgrade or install fails with error

```
ERROR in app: Failed to initialize entry point: EntryPoint(name='invenio_rdm_records', value='invenio_rdm_records:InvenioRDMRecords', group='invenio_base.apps')
Failed to initialize entry point: EntryPoint(name='invenio_rdm_records', value='invenio_rdm_records:InvenioRDMRecords', group='invenio_base.apps')
Traceback (most recent call last):
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/bin/invenio", line 10, in <module>
    sys.exit(cli())
             ~~~^^
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/click/core.py", line 1485, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/click/core.py", line 1406, in main
    rv = self.invoke(ctx)
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/click/core.py", line 1873, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/click/core.py", line 1269, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/click/core.py", line 824, in invoke
    return callback(*args, **kwargs)
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/click/decorators.py", line 34, in new_func
    return f(get_current_context(), *args, **kwargs)
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/flask/cli.py", line 397, in decorator
    app = ctx.ensure_object(ScriptInfo).load_app()
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/flask/cli.py", line 342, in load_app
    app = self.create_app()
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/invenio_base/app.py", line 197, in create_cli_app
    app = create_app(debug=get_debug_flag())
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/invenio_base/app.py", line 127, in _create_app
    app_loader(
    ~~~~~~~~~~^
        app,
        ^^^^
        entry_points=extension_entry_points,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        modules=extensions,
        ^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/invenio_base/app.py", line 235, in app_loader
    _loader(app, lambda ext: ext(app), entry_points=entry_points, modules=modules)
    ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/invenio_base/app.py", line 306, in _loader
    init_func(ep.load())
    ~~~~~~~~~^^^^^^^^^^^
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/invenio_base/app.py", line 235, in <lambda>
    _loader(app, lambda ext: ext(app), entry_points=entry_points, modules=modules)
                             ~~~^^^^^
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/invenio_rdm_records/ext.py", line 98, in __init__
    self.init_app(app)
    ~~~~~~~~~~~~~^^^^^
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/invenio_rdm_records/ext.py", line 106, in init_app
    app.register_blueprint(blueprint)
    ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/flask/sansio/scaffold.py", line 47, in wrapper_func
    return f(self, *args, **kwargs)
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/flask/sansio/app.py", line 595, in register_blueprint
    blueprint.register(self, options)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "/Users/illyriab/Desktop/invenio-repo/chemical-biology/.venv/lib/python3.14/site-packages/flask/sansio/blueprints.py", line 310, in register
    raise ValueError(
    ...<3 lines>...
    )
ValueError: The name 'invenio_rdm_records' is already registered for this blueprint. Use 'name=' to provide a unique name.
```

## Following changes were not commited

Then a metadata model "spectrum" was created extending full RDM model. This can be changed later and is meant as a demo. You can configure the model in the spectrum/metadata.yml

To run this code see [Running an instance of a repository](https://nrp-cz.github.io/docs/installation/run_instance) and make sure you meet the [prerequisites](https://nrp-cz.github.io/docs/installation).

invenio.cfg has been edited because I am on Mac

```
# hack to get invenio working on MacOS 26
import os
os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = "/opt/homebrew/lib"
```