import React from "react";
import PropTypes from "prop-types";
import { getIn, useFormikContext } from "formik";
import {
  RemoteSelectField,
  SelectField,
  TextAreaField as InvenioTextAreaField,
} from "react-invenio-forms";
import { useFieldData, mergeFieldData } from "@js/oarepo_ui/forms";
import { i18next } from "@translations/i18next";
import { COUNTRIES } from "./countries";

export const toOptions = (pairs) =>
  pairs.map(([value, text]) => ({ key: value, value, text }));

/**
 * Select for `keyword` fields with `enum` in the model. Label, help and
 * required flag are taken from the model (metadata.yaml), options must
 * match the enum values there.
 */
export const EnumSelectField = ({
  fieldPath,
  options,
  multiple = false,
  label,
  required,
  helpText,
  ...rest
}) => {
  const { getFieldData } = useFieldData();
  const fieldDataProps = mergeFieldData(
    getFieldData({ fieldPath, icon: "list" }),
    { label, required, helpText },
  );
  return (
    <SelectField
      fieldPath={fieldPath}
      options={options}
      multiple={multiple}
      clearable={!fieldDataProps.required}
      search
      selection
      optimized
      {...fieldDataProps}
      {...rest}
    />
  );
};

EnumSelectField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  options: PropTypes.arrayOf(
    PropTypes.shape({ value: PropTypes.string, text: PropTypes.string }),
  ).isRequired,
  /* eslint-disable react/require-default-props */
  multiple: PropTypes.bool,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  required: PropTypes.bool,
  helpText: PropTypes.string,
  /* eslint-enable react/require-default-props */
};

/** Multi-line text (protocols, conditions); label etc. taken from the model. */
export const TextAreaField = ({ fieldPath, label, required, helpText, ...rest }) => {
  const { getFieldData } = useFieldData();
  const fieldDataProps = mergeFieldData(getFieldData({ fieldPath }), {
    label,
    required,
    helpText,
  });
  return (
    <InvenioTextAreaField
      fieldPath={fieldPath}
      optimized
      rows={4}
      {...fieldDataProps}
      {...rest}
    />
  );
};

TextAreaField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  /* eslint-disable react/require-default-props */
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  required: PropTypes.bool,
  helpText: PropTypes.string,
  /* eslint-enable react/require-default-props */
};

const localizedTitle = (title) =>
  typeof title === "string" ? title : title?.en || Object.values(title || {})[0] || "";

// Label of a vocabulary API hit (title_l10n with the vnd.inveniordm serialization)
// or of a stored value ({id, title} vocabulary item, {title} or {name} free text).
const defaultItemText = (item) =>
  item.title_l10n || localizedTitle(item.title) || item.name || item.id || "";

const defaultFreeTextValue = (text) => ({ title: { en: text } });

const serializeAddedValue = (value) => ({ key: value, value, text: value, freeText: true });

/**
 * Vocabulary select that also accepts values outside the vocabulary. Vocabulary
 * items are stored as {id}, typed in values without an id (by default as
 * {title: {en}}), which the backend accepts without the vocabulary check.
 */
export const FreeTextVocabularyField = ({
  fieldPath,
  vocabularyName,
  suggestionAPIUrl,
  suggestionAPIHeaders = { Accept: "application/vnd.inveniordm.v1+json" },
  itemText = defaultItemText,
  freeTextValue = defaultFreeTextValue,
  multiple = false,
  label,
  required,
  helpText,
  ...rest
}) => {
  const { values } = useFormikContext();
  const { getFieldData } = useFieldData();
  const fieldDataProps = mergeFieldData(getFieldData({ fieldPath, icon: "tag" }), {
    label,
    required,
    helpText,
  });
  const stored = getIn(values, fieldPath);
  const storedItems = multiple ? stored || [] : stored ? [stored] : [];

  // options for API hits and stored values; a value without an id is free text
  const serializeOptions = (items) =>
    items
      .filter((item) => item && (item.id || itemText(item)))
      .map((item) => {
        const text = itemText(item);
        return item.id
          ? { key: item.id, value: item.id, text, id: item.id }
          : { key: text, value: text, text, freeText: true };
      });

  // SUI calls onChange before onAddItem, so a value that is not a known vocabulary
  // suggestion is a newly typed free text value.
  const toStoredValue = (value, suggestions) => {
    const option = suggestions.find((o) => o.value === value);
    return option && !option.freeText ? { id: option.id } : freeTextValue(value);
  };

  const toDropdownValue = (item) => item?.id ?? (item ? itemText(item) : "");

  return (
    <RemoteSelectField
      fieldPath={fieldPath}
      suggestionAPIUrl={suggestionAPIUrl || `/api/vocabularies/${vocabularyName}`}
      suggestionAPIHeaders={suggestionAPIHeaders}
      serializeSuggestions={serializeOptions}
      serializeAddedValue={serializeAddedValue}
      initialSuggestions={storedItems}
      multiple={multiple}
      allowAdditions
      search
      deburr
      clearable={!fieldDataProps.required}
      selectOnBlur={false}
      value={multiple ? storedItems.map(toDropdownValue) : toDropdownValue(stored)}
      onValueChange={({ data, formikProps }, selectedSuggestions) => {
        if (multiple) {
          formikProps.form.setFieldValue(
            fieldPath,
            data.value.map((value) => toStoredValue(value, selectedSuggestions)),
          );
        } else {
          formikProps.form.setFieldValue(
            fieldPath,
            data.value ? toStoredValue(data.value, selectedSuggestions) : undefined,
          );
        }
      }}
      {...fieldDataProps}
      {...rest}
    />
  );
};

FreeTextVocabularyField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  /* eslint-disable react/require-default-props */
  vocabularyName: PropTypes.string,
  suggestionAPIUrl: PropTypes.string,
  suggestionAPIHeaders: PropTypes.object,
  itemText: PropTypes.func,
  freeTextValue: PropTypes.func,
  multiple: PropTypes.bool,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  required: PropTypes.bool,
  helpText: PropTypes.string,
  /* eslint-enable react/require-default-props */
};

const countryOptions = COUNTRIES.map(([code, name]) => ({ key: code, value: code, text: name }));

/** Country select storing the ISO 3166-1 alpha-2 code (e.g. "CZ"). */
export const CountrySelectField = ({ fieldPath, label, ...rest }) => (
  <SelectField
    fieldPath={fieldPath}
    label={label}
    options={countryOptions}
    search
    selection
    clearable
    optimized
    placeholder={i18next.t("Select a country")}
    {...rest}
  />
);

CountrySelectField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  // eslint-disable-next-line react/require-default-props
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
};
