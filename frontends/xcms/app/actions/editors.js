import * as types from '../constants/ActionTypes';

export function addText(label, text) {
  return { type: types.ADD_TEXT, label, text }
}

export function editText(label, text) {
  return { type: types.EDIT_TEXT, label, text }
}

export function deleteText(label) {
  return { type: types.DELETE_TEXT, id}
}