import _isEmpty from "lodash/isEmpty";
import { CCMMDepositRecordSerializer } from "@js/ccmm_invenio/forms";

// role of the person who prepared the sample (CCMM contributor roles vocabulary)
const SAMPLE_PREPARER_ROLE = "DataCollector";

const isFilled = (value) => (typeof value === "string" ? value.trim() !== "" : !_isEmpty(value));

/**
 * Person from the form (one creator / contributor) in the API format, or null
 * when no name was entered.
 */
const serializePerson = (person, role) => {
  const { given_name: givenName, family_name: familyName } = person?.person_or_org || {};
  if (!isFilled(givenName) && !isFilled(familyName)) {
    return null;
  }
  return {
    person_or_org: {
      type: "personal",
      ...(isFilled(givenName) ? { given_name: givenName.trim() } : {}),
      ...(isFilled(familyName) ? { family_name: familyName.trim() } : {}),
    },
    ...(role ? { role: { id: role } } : {}),
    affiliations: (person.affiliations || []).filter(
      (affiliation) => affiliation && (affiliation.id || isFilled(affiliation.name)),
    ),
  };
};

/**
 * CCMM serializer for the dataset form, which has exactly two persons: the PI
 * (the only creator) and the sample preparer (the only contributor, with role
 * Data Collector), and a single geolocation.
 */
export class DatasetDepositRecordSerializer extends CCMMDepositRecordSerializer {
  serialize(record) {
    const serialized = super.serialize(record);
    const metadata = serialized.metadata || {};

    const pi = serializePerson(metadata.creators?.[0]);
    if (pi) {
      metadata.creators = [pi];
    } else {
      delete metadata.creators;
    }

    const samplePreparer = serializePerson(metadata.contributors?.[0], SAMPLE_PREPARER_ROLE);
    if (samplePreparer) {
      metadata.contributors = [samplePreparer];
    } else {
      delete metadata.contributors;
    }

    const location = metadata.locations?.features?.[0];
    if (location && (isFilled(location.place) || isFilled(location.description) || location.geometry)) {
      metadata.locations = { features: [location] };
    } else {
      delete metadata.locations;
    }

    return serialized;
  }
}
