import React from "react";
import PropTypes from "prop-types";
import { SelectField } from "react-invenio-forms";
import { useFieldData, mergeFieldData } from "@js/oarepo_ui/forms";

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
