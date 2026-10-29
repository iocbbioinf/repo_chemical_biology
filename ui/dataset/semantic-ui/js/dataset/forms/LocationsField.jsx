import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { FieldArray, getIn, useFormikContext } from "formik";
import { Form, Icon } from "semantic-ui-react";
import { FieldLabel } from "react-invenio-forms";
import { i18next } from "@translations/i18next";
import { ArrayFieldItem, TextField, useFieldData } from "@js/oarepo_ui/forms";

// GeoJSON point coordinates are [longitude, latitude]
const LONGITUDE = 0;
const LATITUDE = 1;

const toInputValue = (coordinate) => (typeof coordinate === "number" ? String(coordinate) : "");

/**
 * Latitude and longitude inputs editing the GeoJSON point of a location. The
 * point is stored only when both coordinates are numbers; a half filled point
 * is kept in the inputs only (the API rejects incomplete coordinates).
 */
const PointInputs = ({ fieldPath }) => {
  const { values, errors, setFieldValue } = useFormikContext();
  const geometryPath = `${fieldPath}.geometry`;
  const stored = getIn(values, `${geometryPath}.coordinates`);
  const [inputs, setInputs] = useState({
    latitude: toInputValue(stored?.[LATITUDE]),
    longitude: toInputValue(stored?.[LONGITUDE]),
  });

  // follow changes made outside of these inputs (e.g. a removed location above)
  const storedKey = JSON.stringify(stored ?? null);
  useEffect(() => {
    setInputs((current) => {
      if (stored) {
        return { latitude: toInputValue(stored[LATITUDE]), longitude: toInputValue(stored[LONGITUDE]) };
      }
      const complete = current.latitude !== "" && current.longitude !== "";
      return complete ? { latitude: "", longitude: "" } : current;
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [storedKey]);

  const handleChange = (name) => (e, { value }) => {
    const updated = { ...inputs, [name]: value };
    setInputs(updated);
    const latitude = parseFloat(updated.latitude);
    const longitude = parseFloat(updated.longitude);
    setFieldValue(
      geometryPath,
      Number.isFinite(latitude) && Number.isFinite(longitude)
        ? { type: "Point", coordinates: [longitude, latitude] }
        : undefined,
    );
  };

  const incomplete = (inputs.latitude === "") !== (inputs.longitude === "");
  const apiError = getIn(errors, geometryPath);
  const errorMessage = incomplete
    ? i18next.t("Enter both latitude and longitude.")
    : typeof apiError === "string"
      ? apiError
      : undefined;

  return (
    <>
      <Form.Input
        id={`${fieldPath}.latitude`}
        label={i18next.t("Latitude")}
        type="number"
        step="any"
        min={-90}
        max={90}
        width={3}
        value={inputs.latitude}
        onChange={handleChange("latitude")}
        error={errorMessage ? { content: errorMessage, pointing: "above" } : undefined}
      />
      <Form.Input
        id={`${fieldPath}.longitude`}
        label={i18next.t("Longitude")}
        type="number"
        step="any"
        min={-180}
        max={180}
        width={3}
        value={inputs.longitude}
        onChange={handleChange("longitude")}
        error={errorMessage ? true : undefined}
      />
    </>
  );
};

PointInputs.propTypes = {
  fieldPath: PropTypes.string.isRequired,
};

/**
 * Geolocations of the dataset (CCMM/RDM metadata.locations.features): place
 * name, description and an optional point (latitude, longitude).
 */
export const LocationsField = ({ fieldPath = "metadata.locations.features" }) => {
  const { values } = useFormikContext();
  const { getFieldData } = useFieldData();
  const locationsData = getFieldData({ fieldPath: "metadata.locations", icon: "map marker alternate" });
  const features = getIn(values, fieldPath, []);

  return (
    <Form.Field>
      <FieldLabel htmlFor={fieldPath} icon="map marker alternate" label={i18next.t("Geolocation")} />
      <FieldArray
        name={fieldPath}
        render={(arrayHelpers) => (
          <>
            {features.map((feature, index) => {
              const itemPath = `${fieldPath}.${index}`;
              return (
                <ArrayFieldItem
                  // eslint-disable-next-line react/no-array-index-key
                  key={index}
                  indexPath={index}
                  arrayHelpers={arrayHelpers}
                  fieldPathPrefix={itemPath}
                >
                  <TextField fieldPath={`${itemPath}.place`} width={5} />
                  <TextField fieldPath={`${itemPath}.description`} width={4} />
                  <PointInputs fieldPath={itemPath} />
                </ArrayFieldItem>
              );
            })}
            {locationsData.helpText && <label className="helptext">{locationsData.helpText}</label>}
            <Form.Button
              className="array-field-add-button inline"
              type="button"
              icon
              labelPosition="left"
              onClick={() => arrayHelpers.push({ place: "" })}
            >
              <Icon name="add" />
              {i18next.t("Add location")}
            </Form.Button>
          </>
        )}
      />
    </Form.Field>
  );
};

LocationsField.propTypes = {
  // eslint-disable-next-line react/require-default-props
  fieldPath: PropTypes.string,
};
