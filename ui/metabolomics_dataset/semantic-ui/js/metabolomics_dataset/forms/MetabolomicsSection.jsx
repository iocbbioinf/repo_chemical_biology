import React from "react";
import { buildUID } from "react-searchkit";
import Overridable from "react-overridable";
import { Form } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { TextField } from "@js/oarepo_ui/forms";
import { EnumSelectField, toOptions } from "@js/mass_spec";

const fieldPath = "metadata.metabolomics";

// values must match the enums in models/metabolomics_dataset/metadata.yaml
// and the extensions in common/services/ms_files.py
const rawFormatOptions = toOptions([
  ["thermo_raw", "Thermo RAW (.raw)"],
  ["bruker_d", i18next.t("Bruker .d directory, zipped (.d.zip)")],
  ["waters_raw", i18next.t("Waters .raw directory, zipped (.raw.zip)")],
  ["sciex_wiff", "SCIEX WIFF (.wiff, .wiff2, .wiff.scan)"],
  ["agilent_d", i18next.t("Agilent .d directory, zipped (.d.zip)")],
  ["shimadzu_lcd", "Shimadzu (.lcd, .qgd)"],
  ["andi_cdf", "ANDI-MS netCDF (.cdf)"],
]);

const separationOptions = toOptions([
  ["gc", i18next.t("Gas chromatography (GC)")],
  ["lc", i18next.t("Liquid chromatography (LC)")],
  ["ce", i18next.t("Capillary electrophoresis (CE)")],
  ["direct_infusion", i18next.t("Direct infusion")],
]);

/** Deposit form tab with metabolomics specific metadata (MetabolomicsMetadata). */
export const MetabolomicsSection = {
  key: "metabolomics",
  label: i18next.t("Metabolomics"),
  component: (tabConfig) => {
    const { overridableIdPrefix } = tabConfig.formConfig;
    return (
      <Overridable id={buildUID(overridableIdPrefix, "Metabolomics")} {...tabConfig}>
        <>
          <EnumSelectField
            fieldPath={`${fieldPath}.raw_format`}
            options={rawFormatOptions}
          />
          <Form.Group widths="equal">
            <TextField fieldPath={`${fieldPath}.acquisition_software`} />
            <EnumSelectField
              fieldPath={`${fieldPath}.separation`}
              options={separationOptions}
            />
          </Form.Group>
        </>
      </Overridable>
    );
  },
  includesPaths: [fieldPath],
};
