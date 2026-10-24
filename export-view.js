export function openReportDialog({ dialog, scopeControls, allocationOnlyControl, generationStatus }) {
  for (const scopeControl of scopeControls) {
    scopeControl.checked = scopeControl.value === 'portfolio';
  }
  allocationOnlyControl.checked = false;
  generationStatus.textContent = '';
  generationStatus.hidden = true;

  if (typeof dialog.showModal === 'function') {
    dialog.showModal();
  } else {
    dialog.setAttribute('open', '');
  }
}