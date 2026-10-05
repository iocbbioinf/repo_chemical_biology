import React from "react";
import { buildUID } from "react-searchkit";
import Overridable from "react-overridable";
import { Form } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { TextField } from "@js/oarepo_ui/forms";
import { EnumSelectField, toOptions } from "@js/mass_spec";

const fieldPath = "metadata.proteomics";

// values must match the enums in models/proteomics_dataset/metadata.yaml
const digestionEnzymeOptions = toOptions([
  ["trypsin", i18next.t("Trypsin")],
  ["trypsin_lys_c", i18next.t("Trypsin/Lys-C")],
  ["lys_c", "Lys-C"],
  ["chymotrypsin", i18next.t("Chymotrypsin")],
  ["glu_c", "Glu-C"],
  ["asp_n", "Asp-N"],
  ["none", i18next.t("None (top-down)")],
]);

const acquisitionModeOptions = toOptions([
  ["dda", i18next.t("Data-dependent acquisition (DDA)")],
  ["dia", i18next.t("Data-independent acquisition (DIA)")],
  ["prm", i18next.t("Parallel reaction monitoring (PRM)")],
  ["srm", i18next.t("Selected reaction monitoring (SRM)")],
]);

/** Deposit form tab with proteomics specific metadata (ProteomicsMetadata). */
export const ProteomicsSection = {
  key: "proteomics",
  label: i18next.t("Proteomics"),
  component: (tabConfig) => {
    const { overridableIdPrefix } = tabConfig.formConfig;
    return (
      <Overridable id={buildUID(overridableIdPrefix, "Proteomics")} {...tabConfig}>
        <>
          <Form.Group widths="equal">
            <TextField fieldPath={`${fieldPath}.organism`} />
            <TextField fieldPath={`${fieldPath}.ncbi_taxon_id`} />
          </Form.Group>
          <Form.Group widths="equal">
            <EnumSelectField
              fieldPath={`${fieldPath}.digestion_enzyme`}
              options={digestionEnzymeOptions}
            />
            <EnumSelectField
              fieldPath={`${fieldPath}.acquisition_mode`}
              options={acquisitionModeOptions}
            />
          </Form.Group>
        </>
      </Overridable>
    );
  },
  includesPaths: [fieldPath],
};
