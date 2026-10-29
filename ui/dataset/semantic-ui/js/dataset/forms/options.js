import { i18next } from "@translations/i18next";
import { toOptions } from "./fields";

// Option lists for enum fields in models/dataset/metadata.yaml.
// Values must stay in sync with the enum values in the yaml.

export const analysisTypeOptions = toOptions([
  ["general", i18next.t("General")],
  ["microbiology", i18next.t("Microbiology")],
  ["plant_biology", i18next.t("Plant biology")],
  ["clinical", i18next.t("Clinical")],
]);
