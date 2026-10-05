import { i18next } from "@translations/i18next";

// Option lists for enum fields in models/common/mass_spec.yaml.
// Values must stay in sync with the enum values in the yaml.

const toOptions = (pairs) =>
  pairs.map(([value, text]) => ({ key: value, value, text }));

export const instrumentVendorOptions = toOptions([
  ["thermo", "Thermo Fisher Scientific"],
  ["bruker", "Bruker"],
  ["sciex", "SCIEX"],
  ["waters", "Waters"],
  ["agilent", "Agilent"],
  ["shimadzu", "Shimadzu"],
  ["other", i18next.t("Other")],
]);

export const ionizationSourceOptions = toOptions([
  ["esi", i18next.t("Electrospray (ESI)")],
  ["nano_esi", i18next.t("Nano-electrospray (nanoESI)")],
  ["apci", i18next.t("Atmospheric pressure chemical ionization (APCI)")],
  ["appi", i18next.t("Atmospheric pressure photoionization (APPI)")],
  ["maldi", "MALDI"],
  ["ei", i18next.t("Electron ionization (EI)")],
  ["ci", i18next.t("Chemical ionization (CI)")],
]);

export const polarityOptions = toOptions([
  ["positive", i18next.t("Positive")],
  ["negative", i18next.t("Negative")],
  ["switching", i18next.t("Polarity switching")],
]);

export const massAnalyzerOptions = toOptions([
  ["quadrupole", i18next.t("Quadrupole")],
  ["ion_trap", i18next.t("Ion trap")],
  ["orbitrap", "Orbitrap"],
  ["tof", i18next.t("Time of flight (TOF)")],
  ["fticr", "FT-ICR"],
  ["ion_mobility", i18next.t("Ion mobility")],
  ["magnetic_sector", i18next.t("Magnetic sector")],
]);

export { toOptions };
