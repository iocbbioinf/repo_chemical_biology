import { DepositFormApp, parseFormAppConfig } from "@js/oarepo_ui/forms";
import React from "react";
import ReactDOM from "react-dom";
import { EDTFSingleDatePicker } from "@js/oarepo_ui/forms";
import { parametrize } from "react-overridable";
import { DatasetDepositRecordSerializer } from "./DatasetDepositRecordSerializer";
import {
  GeneralInformationSection,
  CCMMFiles,
  CCMMCommunityAndAccess,
} from "./GeneralInformationSection";

const { rootEl, config, ...rest } = parseFormAppConfig();

// Only three tabs: general information (incl. persons, sample and analysis),
// files and community & access. CCMM funding, alternative identifiers and
// related works tabs are not used.
const sections = [GeneralInformationSection, CCMMFiles, CCMMCommunityAndAccess];
const recordSerializer = new DatasetDepositRecordSerializer(
  config.default_locale,
  config.custom_fields.vocabularies,
);

const parametrizeEDTFSingleDatePicker = parametrize(EDTFSingleDatePicker, {
  customInputProps: { width: 16 },
});

export const componentOverrides = {
  "InvenioRdmRecords.DepositForm.DatesField.DateField":
    parametrizeEDTFSingleDatePicker,
};

ReactDOM.render(
  <DepositFormApp
    config={config}
    {...rest}
    sections={sections}
    recordSerializer={recordSerializer}
    componentOverrides={componentOverrides}
    useWizardForm
  />,
  rootEl,
);
