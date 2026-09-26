// Small interactions kept framework-free for the academic project.
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('form[data-confirm]').forEach((form) => {
    form.addEventListener('submit', (event) => {
      if (!window.confirm(form.dataset.confirm)) event.preventDefault();
    });
  });

  document.querySelectorAll('.dismiss').forEach((button) => {
    button.addEventListener('click', () => button.closest('.flash')?.remove());
  });

  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav-links');
  toggle?.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });

  const donorSelect = document.querySelector('#donor-select');
  const groupField = document.querySelector('#donor-group');
  const groupHint = document.querySelector('#selected-group');
  const updateGroup = () => {
    const selected = donorSelect?.selectedOptions[0];
    const group = selected?.dataset.group || '';
    if (groupField) groupField.value = group;
    if (groupHint) groupHint.textContent = group ? `Selected donor's blood group: ${group}` : 'Select a donor to view their blood group.';
  };
  donorSelect?.addEventListener('change', updateGroup);
  updateGroup();
});
