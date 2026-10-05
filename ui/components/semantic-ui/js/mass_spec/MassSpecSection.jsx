import React from "react";
import { buildUID } from "react-searchkit";
import Overridable from "react-overridable";
import { Form } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { TextField } from "@js/oarepo_ui/forms";
import { EnumSelectField } from "./EnumSelectField";
import {
  instrumentVendorOptions,
  ionizationSourceOptions,
  polarityOptions,
  massAnalyzerOptions,
} from "./options";

const fieldPath = "metadata.mass_spec";

/** Deposit form tab with metadata shared by all mass spectra models (MassSpecCommon). */
export const MassSpecSection = {
  key: "mass-spec",
  label: i18next.t("Mass spectrometry"),
  component: (tabConfig) => {
    const { overridableIdPrefix } = tabConfig.formConfig;
    return (
      <Overridable id={buildUID(overridableIdPrefix, "MassSpec")} {...tabConfig}>
        <>
          <Form.Group widths="equal">
            <EnumSelectField
              fieldPath={`${fieldPath}.instrument_vendor`}
              options={instrumentVendorOptions}
            />
            <TextField fieldPath={`${fieldPath}.instrument_model`} />
          </Form.Group>
          <Form.Group widths="equal">
            <EnumSelectField
              fieldPath={`${fieldPath}.ionization_source`}
              options={ionizationSourceOptions}
            />
            <EnumSelectField
              fieldPath={`${fieldPath}.polarity`}
              options={polarityOptions}
            />
          </Form.Group>
          <EnumSelectField
            fieldPath={`${fieldPath}.mass_analyzers`}
            options={massAnalyzerOptions}
            multiple
          />
          <Form.Group widths="equal">
            <TextField fieldPath={`${fieldPath}.mz_range.min`} type="number" step="any" />
            <TextField fieldPath={`${fieldPath}.mz_range.max`} type="number" step="any" />
          </Form.Group>
        </>
      </Overridable>
    );
  },
  includesPaths: [fieldPath],
};
