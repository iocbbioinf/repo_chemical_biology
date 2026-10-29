import React from "react";
import { buildUID } from "react-searchkit";
import Overridable from "react-overridable";
import { Form } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { TextField } from "@js/oarepo_ui/forms";

/**
 * Deposit form tab with contact e-mails. The principal investigator and the
 * sample preparer themselves are CCMM contributors (roles Project Leader and
 * Data Collector), which do not carry e-mails.
 */
export const ContactsSection = {
  key: "contacts",
  label: i18next.t("Contacts"),
  component: (tabConfig) => {
    const { overridableIdPrefix } = tabConfig.formConfig;
    return (
      <Overridable id={buildUID(overridableIdPrefix, "Contacts")} {...tabConfig}>
        <Form.Group widths="equal">
          <TextField fieldPath="metadata.principal_investigator_email" type="email" />
          <TextField fieldPath="metadata.sample_preparer_email" type="email" />
        </Form.Group>
      </Overridable>
    );
  },
  includesPaths: ["metadata.principal_investigator_email", "metadata.sample_preparer_email"],
};
