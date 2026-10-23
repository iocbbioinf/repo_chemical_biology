import { DepositFormApp, parseFormAppConfig } from "@js/oarepo_ui/forms";
import React from "react";
import ReactDOM from "react-dom";
import { EDTFSingleDatePicker } from "@js/oarepo_ui/forms";
import { parametrize } from "react-overridable";
import {
  CCMMDepositRecordSerializer,
  CCMMSections,
} from "@js/ccmm_invenio/forms";
import { SampleSection } from "./SampleSection";
import { ContactsSection } from "./ContactsSection";

const { rootEl, config, ...rest } = parseFormAppConfig();

// CCMM sections (general information, files, ...) followed by the dataset specific ones
const sections = [...CCMMSections, SampleSection, ContactsSection];
const recordSerializer = new CCMMDepositRecordSerializer(
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
