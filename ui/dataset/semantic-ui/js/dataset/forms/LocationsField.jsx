import React, { useEffect, useRef, useState } from "react";
import PropTypes from "prop-types";
import { getIn, useFormikContext } from "formik";
import { Button, Form, Message } from "semantic-ui-react";
import { FieldLabel } from "react-invenio-forms";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { i18next } from "@translations/i18next";
import { TextField } from "@js/oarepo_ui/forms";

// GeoJSON point coordinates are [longitude, latitude]
const LONGITUDE = 0;
const LATITUDE = 1;

const DEFAULT_VIEW = { center: [49.8, 15.5], zoom: 6 }; // Czechia
const POINT_ZOOM = 12;

const NOMINATIM_URL = "https://nominatim.openstreetmap.org/search";

const toInputValue = (coordinate) => (typeof coordinate === "number" ? String(coordinate) : "");
const round = (value) => Math.round(value * 1e6) / 1e6;

/** Leaflet map showing the point; a click on the map moves the point there. */
const PointMap = ({ point, onPick }) => {
  const containerRef = useRef(null);
  const mapRef = useRef(null);
  const markerRef = useRef(null);
  const onPickRef = useRef(onPick);
  onPickRef.current = onPick;

  useEffect(() => {
    const map = L.map(containerRef.current).setView(DEFAULT_VIEW.center, DEFAULT_VIEW.zoom);
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);
    map.on("click", (e) => onPickRef.current(round(e.latlng.lat), round(e.latlng.lng)));
    mapRef.current = map;
    return () => map.remove();
  }, []);

  const [latitude, longitude] = point || [];
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;
    if (point) {
      if (markerRef.current) {
        markerRef.current.setLatLng([latitude, longitude]);
      } else {
        // circle marker needs no image assets (default marker icons break with bundlers)
        markerRef.current = L.circleMarker([latitude, longitude], {
          radius: 8,
          weight: 2,
          color: "#d01919",
          fillOpacity: 0.6,
        }).addTo(map);
      }
      if (!map.getBounds().contains([latitude, longitude])) {
        map.setView([latitude, longitude], Math.max(map.getZoom(), POINT_ZOOM));
      }
    } else if (markerRef.current) {
      markerRef.current.remove();
      markerRef.current = null;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [latitude, longitude]);

  return <div ref={containerRef} style={{ height: "320px", width: "100%" }} />;
};

PointMap.propTypes = {
  // eslint-disable-next-line react/require-default-props
  point: PropTypes.arrayOf(PropTypes.number),
  onPick: PropTypes.func.isRequired,
};

/**
 * Geolocation of the dataset: one location (CCMM/RDM metadata.locations.features[0])
 * with place name, description and a point. The point can be picked on the map,
 * found by the place name (OpenStreetMap Nominatim) or typed in. It is stored as a
 * GeoJSON point only when both coordinates are numbers.
 */
export const LocationsField = ({ fieldPath = "metadata.locations.features.0" }) => {
  const { values, errors, setFieldValue } = useFormikContext();
  const geometryPath = `${fieldPath}.geometry`;
  const stored = getIn(values, `${geometryPath}.coordinates`);
  const [inputs, setInputs] = useState({
    latitude: toInputValue(stored?.[LATITUDE]),
    longitude: toInputValue(stored?.[LONGITUDE]),
  });
  const [searching, setSearching] = useState(false);
  const [searchMessage, setSearchMessage] = useState(null);

  const setPoint = (latitude, longitude) => {
    setInputs({ latitude: toInputValue(latitude), longitude: toInputValue(longitude) });
    setFieldValue(geometryPath, { type: "Point", coordinates: [longitude, latitude] });
  };

  const clearPoint = () => {
    setInputs({ latitude: "", longitude: "" });
    setFieldValue(geometryPath, undefined);
  };

  const handleInputChange = (name) => (e, { value }) => {
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

  const findPlace = async () => {
    const place = (getIn(values, `${fieldPath}.place`) || "").trim();
    if (!place) return;
    setSearching(true);
    setSearchMessage(null);
    try {
      const params = new URLSearchParams({ q: place, format: "jsonv2", limit: "1" });
      const response = await fetch(`${NOMINATIM_URL}?${params}`, {
        headers: { "Accept-Language": "en" },
      });
      const results = response.ok ? await response.json() : [];
      if (results.length) {
        setPoint(round(parseFloat(results[0].lat)), round(parseFloat(results[0].lon)));
        setSearchMessage({ positive: true, text: results[0].display_name });
      } else {
        setSearchMessage({ negative: true, text: i18next.t("Place not found.") });
      }
    } catch (e) {
      setSearchMessage({ negative: true, text: i18next.t("Place search is not available.") });
    } finally {
      setSearching(false);
    }
  };

  const point =
    Array.isArray(stored) && stored.length === 2 ? [stored[LATITUDE], stored[LONGITUDE]] : null;
  const incomplete = (inputs.latitude === "") !== (inputs.longitude === "");
  const apiError = getIn(errors, geometryPath);
  const errorMessage = incomplete
    ? i18next.t("Enter both latitude and longitude.")
    : typeof apiError === "string"
      ? apiError
      : undefined;

  return (
    <Form.Field>
      <FieldLabel htmlFor={fieldPath} icon="map marker alternate" label={i18next.t("Geolocation")} />
      <Form.Group>
        <TextField
          fieldPath={`${fieldPath}.place`}
          label={i18next.t("Place")}
          width={8}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              findPlace();
            }
          }}
        />
        <Form.Field width={4}>
          {/* eslint-disable-next-line jsx-a11y/label-has-associated-control */}
          <label>&nbsp;</label>
          <Button
            type="button"
            icon="search"
            content={i18next.t("Find on map")}
            loading={searching}
            onClick={findPlace}
          />
        </Form.Field>
      </Form.Group>
      {searchMessage && (
        <Message size="tiny" positive={searchMessage.positive} negative={searchMessage.negative}>
          {searchMessage.text}
        </Message>
      )}
      <PointMap point={point} onPick={setPoint} />
      <label className="helptext">{i18next.t("Click on the map to set the point.")}</label>
      <Form.Group className="rel-mt-1">
        <Form.Input
          id={`${fieldPath}.latitude`}
          label={i18next.t("Latitude")}
          type="number"
          step="any"
          min={-90}
          max={90}
          width={4}
          value={inputs.latitude}
          onChange={handleInputChange("latitude")}
          error={errorMessage ? { content: errorMessage, pointing: "above" } : undefined}
        />
        <Form.Input
          id={`${fieldPath}.longitude`}
          label={i18next.t("Longitude")}
          type="number"
          step="any"
          min={-180}
          max={180}
          width={4}
          value={inputs.longitude}
          onChange={handleInputChange("longitude")}
          error={errorMessage ? true : undefined}
        />
        <Form.Field width={4}>
          {/* eslint-disable-next-line jsx-a11y/label-has-associated-control */}
          <label>&nbsp;</label>
          <Button
            type="button"
            basic
            icon="close"
            content={i18next.t("Clear point")}
            onClick={clearPoint}
            disabled={!point && !inputs.latitude && !inputs.longitude}
          />
        </Form.Field>
      </Form.Group>
      <TextField fieldPath={`${fieldPath}.description`} label={i18next.t("Location description")} />
    </Form.Field>
  );
};

LocationsField.propTypes = {
  // eslint-disable-next-line react/require-default-props
  fieldPath: PropTypes.string,
};
