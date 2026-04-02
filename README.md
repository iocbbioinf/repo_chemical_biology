# Repository for Chemical Biology Data

**The mass spectra repository will be a platform that enables similarity-based spectrum searches using various algorithms. The handling of data and metadata will be built on FAIR principles.**

This codebase was created following [this tutorial](https://nrp-cz.github.io/docs/installation/create_instance).

A metadata model "spectrum" was created by extending the full RDM model `./run.sh model create spectrum`. It can be configured in the file spectrum/metadata.yml and its UI can be defined in the ui/spectrum directory

Final destination repo: https://github.com/iocbbioinf/repo_chemical_biology

To run this code see [Running an instance of a repository](https://nrp-cz.github.io/docs/installation/run_instance) and make sure you meet the [prerequisites](https://nrp-cz.github.io/docs/installation). Pay attention to python version (3.13), it does not work on version 14!
