import React from "react";
import { Header } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { CCMMSections } from "@js/ccmm_invenio/forms";
import { SampleSection } from "./SampleSection";
import { ContactsSection } from "./ContactsSection";
import { LocationsField } from "./LocationsField";

const ccmmSection = (key) => CCMMSections.find((section) => section.key === key);

const CCMMGeneralInformation = ccmmSection("general-information");
export const CCMMFiles = ccmmSection("files");
export const CCMMCommunityAndAccess = ccmmSection("community-and-access");

/**
 * General information tab: CCMM general information and geolocation, followed
 * by the sample and analysis metadata and the contacts, all in one tab.
 */
export const GeneralInformationSection = {
  ...CCMMGeneralInformation,
  component: (tabConfig) => (
    <>
      <CCMMGeneralInformation.component {...tabConfig} />
      <LocationsField />
      <Header as="h2" size="medium" dividing className="rel-mt-2">
        {SampleSection.label}
      </Header>
      <SampleSection.component {...tabConfig} />
      <Header as="h2" size="medium" dividing className="rel-mt-2">
        {i18next.t("Contacts")}
      </Header>
      <ContactsSection.component {...tabConfig} />
    </>
  ),
  includesPaths: [
    ...CCMMGeneralInformation.includesPaths,
    "metadata.locations",
    ...SampleSection.includesPaths,
    ...ContactsSection.includesPaths,
  ],
};
