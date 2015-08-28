import * as ActionTypes from '../actions';
import { combineReducers } from 'redux';

/**
 * Updates error message to notify about the failed fetches.
 */
export function errorMessage(state = null, action) {
  const { type, error } = action;

  if (type === ActionTypes.RESET_ERROR_MESSAGE) {
    return null;
  } else if (error) {
    return {text: action.error, log: action.log};
  }

  return state;
}

import { ADD_TEXT, EDIT_TEXT, DELETE_TEXT } from '../constants/ActionTypes';

const initialState = [{
  text: 'Use Redux',
  label: 'EDITORs'
}];

export function editors(state = initialState, action) {
  switch (action.type) {
    case ADD_TEXT:
    return [{
      label: action.label,
      text: action.text
    }, ...state];

    case EDIT_TEXT:
    return state.map(editor => Object.assign({}, editor, { label: "edit Text", text: action.text }));

    case DELETE_TEXT:
    return state.map(editor => Object.assign({}, editor, { label: "delete Text", text: action.text }));

    default:
    return state;
  }
}