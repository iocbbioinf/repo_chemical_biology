import React from "react";
import { buildUID } from "react-searchkit";
import Overridable from "react-overridable";
import { getIn, useFormikContext } from "formik";
import { Form, Header } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { TextField, StringArrayField } from "@js/oarepo_ui/forms";
import { EnumSelectField, TextAreaField } from "./fields";
import { domainTypeOptions, analysisTypeOptions } from "./options";

const MicrobiologyFields = () => (
  <>
    <Header as="h3" size="small">
      {i18next.t("Microbiology")}
    </Header>
    <TextField fieldPath="metadata.microbiology.species_name" />
    <TextAreaField fieldPath="metadata.microbiology.cultivation_conditions" />
    <TextAreaField fieldPath="metadata.microbiology.extraction_protocol" />
  </>
);

const PlantBiologyFields = () => (
  <>
    <Header as="h3" size="small">
      {i18next.t("Plant biology")}
    </Header>
    <Form.Group widths="equal">
      <TextField fieldPath="metadata.plant_biology.species_name" />
      <TextField fieldPath="metadata.plant_biology.tissue" />
    </Form.Group>
    <TextAreaField fieldPath="metadata.plant_biology.collection_protocol" />
    <TextAreaField fieldPath="metadata.plant_biology.extraction_protocol" />
  </>
);

const SampleFields = () => {
  const { values } = useFormikContext();
  const analysisType = getIn(values, "metadata.analysis_type");
  return (
    <>
      <Form.Group widths="equal">
        <EnumSelectField
          fieldPath="metadata.domain_type"
          options={domainTypeOptions}
        />
        <EnumSelectField
          fieldPath="metadata.analysis_type"
          options={analysisTypeOptions}
        />
      </Form.Group>
      <Form.Group widths="equal">
        <TextField fieldPath="metadata.sample_type" />
        <TextField fieldPath="metadata.tissue_type" />
      </Form.Group>
      <StringArrayField
        fieldPath="metadata.post_translational_modifications"
        addButtonLabel={i18next.t("Add modification")}
      />
      {/* analysis specific metadata, shown only for the selected type of analysis */}
      {analysisType === "microbiology" && <MicrobiologyFields />}
      {analysisType === "plant_biology" && <PlantBiologyFields />}
    </>
  );
};

/** Deposit form tab with sample and analysis metadata. */
export const SampleSection = {
  key: "sample",
  label: i18next.t("Sample and analysis"),
  component: (tabConfig) => {
    const { overridableIdPrefix } = tabConfig.formConfig;
    return (
      <Overridable id={buildUID(overridableIdPrefix, "Sample")} {...tabConfig}>
        <SampleFields />
      </Overridable>
    );
  },
  includesPaths: [
    "metadata.domain_type",
    "metadata.analysis_type",
    "metadata.sample_type",
    "metadata.tissue_type",
    "metadata.post_translational_modifications",
    "metadata.microbiology",
    "metadata.plant_biology",
  ],
};
