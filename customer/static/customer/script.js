// Shared behaviour for login.html and register.html
// Safe to include on both pages: every block checks the element exists first.

(function () {
  // ---- password show/hide (SVG eye icon toggle) ----
  document.querySelectorAll('.toggle-visibility').forEach((btn) => {
    btn.addEventListener('click', () => {
      const target = document.getElementById(btn.dataset.target);
      if (!target) return;
      const willShow = target.type === 'password';
      target.type = willShow ? 'text' : 'password';
      btn.setAttribute('data-visible', String(willShow));
      btn.setAttribute('aria-label', willShow ? 'Hide password' : 'Show password');
    });
  });

  function setHint(inputId, msg, isError) {
    const hintEl = document.querySelector(`[data-hint-for="${inputId}"]`);
    if (!hintEl) return;
    hintEl.textContent = msg || '';
    hintEl.classList.toggle('error', !!isError);
  }

  // ---- login form ----
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const username = document.getElementById('login-username');
      const password = document.getElementById('login-password');
      username.classList.add('touched');
      password.classList.add('touched');

      let ok = true;
      if (!username.value.trim()) ok = false;

      if (password.value.length < 8) {
        setHint('login-password', 'Password must be at least 8 characters.', true);
        ok = false;
      } else {
        setHint('login-password', '', false);
      }

      const status = document.getElementById('login-status');
      status.classList.remove('ok', 'bad');
      if (ok) {
        status.textContent = 'Signed in — welcome back, ' + username.value.trim() + '.';
        status.classList.add('show', 'ok');
      } else {
        status.textContent = 'Please fill in both fields correctly.';
        status.classList.add('show', 'bad');
      }
    });
  }

  // ---- register form ----
  const registerForm = document.getElementById('register-form');
  if (registerForm) {
    const regPassword = document.getElementById('reg-password');
    const regConfirm = document.getElementById('reg-confirm');
    const regEmail = document.getElementById('reg-email');
    const regUsername = document.getElementById('reg-username');
    const regPhone = document.getElementById('reg-number');

    const USERNAME_MIN = 3;
    const USERNAME_MAX = 20; // "must be less than 15"

    function checkConfirmMatch() {
      if (regConfirm.value && regPassword.value !== regConfirm.value) {
        setHint('reg-confirm', 'Passwords do not match.', true);
        return false;
      }
      setHint('reg-confirm', 'At least 8 characters. Both passwords must match.', false);
      return true;
    }
    regConfirm.addEventListener('input', checkConfirmMatch);
    regPassword.addEventListener('input', checkConfirmMatch);

    regEmail.addEventListener('blur', () => {
      regEmail.classList.add('touched');
      const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(regEmail.value.trim());
      setHint('reg-email', ok || !regEmail.value ? '' : 'Enter a valid email address.', !ok && !!regEmail.value);
    });

    regUsername.addEventListener('blur', () => {
      regUsername.classList.add('touched');
      const val = regUsername.value.trim();
      const ok = new RegExp(`^[A-Za-z0-9_]{${USERNAME_MIN},${USERNAME_MAX}}$`).test(val);
      setHint(
        'reg-username',
        ok || !val
          ? 'Letters, numbers, or underscore only.'
          : `Under ${USERNAME_MAX + 1} characters — letters, numbers, or underscore.`,
        !ok && !!val
      );
    });

    if (regPhone) {
      regPhone.addEventListener('blur', () => {
        regPhone.classList.add('touched');
        const val = regPhone.value.trim();
        const ok = /^\d{10}$/.test(val);
        setHint('reg-number', ok || !val ? 'Enter a 10-digit phone number.' : 'Phone number must be exactly 10 digits.', !ok && !!val);
      });
      // only allow digits as the person types, capped at 10
      regPhone.addEventListener('input', () => {
        regPhone.value = regPhone.value.replace(/\D/g, '').slice(0, 10);
      });
    }

    registerForm.addEventListener('submit', (e) => {
      const fullname = document.getElementById('reg-fullname');
      const touched = [fullname, regEmail, regUsername, regPassword, regConfirm];
      if (regPhone) touched.push(regPhone);
      touched.forEach((el) => el.classList.add('touched'));

      let ok = true;
      if (fullname.value.trim().length < 2) ok = false;

      const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(regEmail.value.trim());
      if (!emailOk) {
        setHint('reg-email', 'Enter a valid email address.', true);
        ok = false;
      }

      const userOk = new RegExp(`^[A-Za-z0-9_]{${USERNAME_MIN},${USERNAME_MAX}}$`).test(regUsername.value.trim());
      if (!userOk) {
        setHint('reg-username', `Under ${USERNAME_MAX + 1} characters — letters, numbers, or underscore.`, true);
        ok = false;
      }

      if (regPhone) {
        const phoneOk = /^\d{10}$/.test(regPhone.value.trim());
        if (!phoneOk) {
          setHint('reg-number', 'Phone number must be exactly 10 digits.', true);
          ok = false;
        }
      }

      if (regPassword.value.length < 8) ok = false;
      if (!checkConfirmMatch()) ok = false;

      // client-side checks only block obviously-invalid submissions;
      // once everything here passes, the form posts to the server as
      // normal and the backend's own messages render in #register-status.
      if (!ok) e.preventDefault();
    });
  }
})();
