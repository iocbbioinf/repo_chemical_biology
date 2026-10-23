import { i18next } from "@translations/i18next";
import { toOptions } from "./fields";

// Option lists for enum fields in models/dataset/metadata.yaml.
// Values must stay in sync with the enum values in the yaml.

export const domainTypeOptions = toOptions([
  ["proteomics", i18next.t("Proteomics")],
  ["metabolomics", i18next.t("Metabolomics")],
  ["lipidomics", i18next.t("Lipidomics")],
  ["other", i18next.t("Other")],
]);

export const analysisTypeOptions = toOptions([
  ["general", i18next.t("General")],
  ["microbiology", i18next.t("Microbiology")],
  ["plant_biology", i18next.t("Plant biology")],
  ["clinical", i18next.t("Clinical")],
]);
