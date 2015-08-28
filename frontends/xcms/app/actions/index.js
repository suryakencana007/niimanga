export const RESET_ERROR_MESSAGE = 'RESET_ERROR_MESSAGE';
export const MESSAGE_BOX = 'MESSAGE_BOX';

/**
 * Resets the currently visible error message.
 *
 */

 export function resetErrorMessage() {
  return {
    type: RESET_ERROR_MESSAGE
  };
}


export function MessageBox(text, log = 'info') {
  return {
    type: MESSAGE_BOX,
    error: text,
    log: log
  };
}