import React from "react";
import PropTypes from "prop-types";
import { Form, Header } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { TextField } from "@js/oarepo_ui/forms";
import { CountrySelectField, FreeTextVocabularyField } from "./fields";

/**
 * One person of the dataset. Name and institution are the CCMM person
 * (personPath = creator or contributor; institution is its affiliation, from
 * ROR or free text), e-mail and country are dataset fields (emailPath,
 * countryPath), as CCMM/RDM persons do not have them.
 * DatasetDepositRecordSerializer completes the person (type, role) on save.
 */
export const PersonFields = ({ title, personPath, emailPath, countryPath, required = false }) => (
  <>
    <Header as="h3" size="small">
      {title}
    </Header>
    <Form.Group widths="equal">
      <TextField
        fieldPath={`${personPath}.person_or_org.given_name`}
        label={i18next.t("First name")}
      />
      <TextField
        fieldPath={`${personPath}.person_or_org.family_name`}
        label={i18next.t("Last name")}
        required={required}
      />
      <TextField
        fieldPath={emailPath}
        label={i18next.t("E-mail")}
        type="email"
        required={required}
      />
    </Form.Group>
    <Form.Group widths="equal">
      <FreeTextVocabularyField
        fieldPath={`${personPath}.affiliations.0`}
        suggestionAPIUrl="/api/affiliations"
        suggestionAPIHeaders={{ Accept: "application/json" }}
        freeTextValue={(name) => ({ name })}
        label={i18next.t("Institution")}
        helpText={i18next.t("Search the Research Organization Registry (ROR) or type the name.")}
        icon="building"
      />
      <CountrySelectField fieldPath={countryPath} label={i18next.t("Country")} />
    </Form.Group>
  </>
);

PersonFields.propTypes = {
  title: PropTypes.string.isRequired,
  personPath: PropTypes.string.isRequired,
  emailPath: PropTypes.string.isRequired,
  countryPath: PropTypes.string.isRequired,
  // eslint-disable-next-line react/require-default-props
  required: PropTypes.bool,
};
