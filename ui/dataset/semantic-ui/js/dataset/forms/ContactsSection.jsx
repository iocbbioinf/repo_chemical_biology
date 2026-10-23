import React from "react";
import PropTypes from "prop-types";
import { buildUID } from "react-searchkit";
import Overridable from "react-overridable";
import { Form, Header } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { TextField } from "@js/oarepo_ui/forms";

/** Fields of a ContactPerson (models/dataset/metadata.yaml). */
const ContactPersonFields = ({ fieldPath, title }) => (
  <>
    <Header as="h3" size="small">
      {title}
    </Header>
    <Form.Group widths="equal">
      <TextField fieldPath={`${fieldPath}.name`} />
      <TextField fieldPath={`${fieldPath}.email`} type="email" />
    </Form.Group>
    <Form.Group widths="equal">
      <TextField fieldPath={`${fieldPath}.institution`} />
      <TextField fieldPath={`${fieldPath}.country`} />
    </Form.Group>
  </>
);

ContactPersonFields.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
};

/** Deposit form tab with the principal investigator and sample preparer. */
export const ContactsSection = {
  key: "contacts",
  label: i18next.t("Contacts"),
  component: (tabConfig) => {
    const { overridableIdPrefix } = tabConfig.formConfig;
    return (
      <Overridable id={buildUID(overridableIdPrefix, "Contacts")} {...tabConfig}>
        <>
          <ContactPersonFields
            fieldPath="metadata.principal_investigator"
            title={i18next.t("Principal investigator")}
          />
          <ContactPersonFields
            fieldPath="metadata.sample_prepared_by"
            title={i18next.t("Sample prepared by")}
          />
        </>
      </Overridable>
    );
  },
  includesPaths: ["metadata.principal_investigator", "metadata.sample_prepared_by"],
};
