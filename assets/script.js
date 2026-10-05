const navToggle = document.querySelector("[data-nav-toggle]");
const siteNav = document.querySelector("[data-site-nav]");
const supportForms = Array.from(
  document.querySelectorAll("[data-support-request-form]"),
);

if (siteNav) {
  const currentPath = window.location.pathname.replace(/\/$/, "") || "/";
  siteNav.querySelectorAll("a[href]").forEach((link) => {
    const linkUrl = new URL(link.href, window.location.origin);
    const linkPath = linkUrl.pathname.replace(/\/$/, "") || "/";
    if (linkPath === currentPath && !linkUrl.hash)
      link.setAttribute("aria-current", "page");
  });
}

function closeMenu() {
  if (!navToggle || !siteNav) return;
  siteNav.classList.remove("is-open");
  navToggle.setAttribute("aria-expanded", "false");
  document.body.classList.remove("menu-open");
}

function openMenu() {
  if (!navToggle || !siteNav) return;
  siteNav.classList.add("is-open");
  navToggle.setAttribute("aria-expanded", "true");
  document.body.classList.add("menu-open");
}

if (navToggle && siteNav) {
  navToggle.addEventListener("click", () => {
    if (siteNav.classList.contains("is-open")) {
      closeMenu();
    } else {
      openMenu();
    }
  });

  siteNav.addEventListener("click", (event) => {
    if (event.target instanceof HTMLAnchorElement) closeMenu();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu();
  });

  document.addEventListener("click", (event) => {
    if (!siteNav.classList.contains("is-open")) return;
    if (siteNav.contains(event.target) || navToggle.contains(event.target))
      return;
    closeMenu();
  });
}

function setupRevealMotion() {
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const revealSelectors = [
    ".section-heading",
    ".v36-common-call-card",
    ".home-support-proof-card",
    ".home-process-grid article",
    ".countup-stat",
    ".quick-path-card",
    ".problem-link-card",
    ".technical-proof-card",
    ".proof-static-grid figure",
    ".work-photo-card",
    ".service-card",
    ".card",
  ].join(",");
  const revealItems = Array.from(document.querySelectorAll(revealSelectors));

  if (!revealItems.length || reducedMotion.matches) {
    revealItems.forEach((item) => item.classList.add("is-visible"));
    return;
  }

  document.documentElement.classList.add("js-reveal-enabled");

  const staggerGroups = [
    ".common-call-grid--v36 .v36-common-call-card",
    ".home-support-proof-grid .home-support-proof-card",
    ".home-process-grid article",
    ".home-countup-stats .countup-stat",
    ".quick-path-grid .quick-path-card",
    ".problem-link-grid .problem-link-card",
    ".proof-static-grid figure",
  ];

  revealItems.forEach((item) => {
    item.classList.add("reveal-item");
    item.style.setProperty("--reveal-delay", "0ms");
  });

  staggerGroups.forEach((selector) => {
    Array.from(document.querySelectorAll(selector)).forEach((item, index) => {
      item.style.setProperty("--reveal-delay", `${Math.min(index * 80, 420)}ms`);
    });
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        const delayText = getComputedStyle(entry.target).getPropertyValue("--reveal-delay");
        const delay = Number.parseFloat(delayText) || 0;
        window.setTimeout(
          () => entry.target.style.setProperty("--reveal-delay", "0ms"),
          delay + 620,
        );
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.18, rootMargin: "0px 0px -8% 0px" },
  );

  revealItems.forEach((item) => observer.observe(item));
}

const proofRails = Array.from(document.querySelectorAll("[data-proof-rail]"));

if (proofRails.length) {
  document.documentElement.classList.add("js-carousel-enabled");
}

proofRails.forEach((rail) => {
  const slides = Array.from(rail.querySelectorAll("[data-proof-slide]"));
  const dots = Array.from(rail.querySelectorAll("[data-proof-dot]"));
  const previous = rail.querySelector("[data-proof-prev]");
  const next = rail.querySelector("[data-proof-next]");
  const pause = rail.querySelector("[data-proof-pause]");
  const currentNumber = rail.querySelector("[data-proof-current]");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let current = 0;
  let timer = null;
  let userPaused = false;
  let interactionHydrated = false;

  function hydrateSlideImage(slide) {
    const images = Array.from(slide?.querySelectorAll?.("img[data-src]") || []);
    images.forEach((image) => {
      const nextSrc = image.dataset.src;
      if (!nextSrc) return;
      if (image.dataset.srcset) image.srcset = image.dataset.srcset;
      if (image.dataset.sizes) image.sizes = image.dataset.sizes;
      image.src = nextSrc;
      image.removeAttribute("data-src");
      image.removeAttribute("data-srcset");
      image.removeAttribute("data-sizes");
    });
  }

  function slideAt(index) {
    if (!slides.length) return null;
    return slides[(index + slides.length) % slides.length];
  }

  function hydrateSlideAt(index) {
    hydrateSlideImage(slideAt(index));
  }

  function hydrateAllSlides() {
    slides.forEach(hydrateSlideImage);
    interactionHydrated = true;
  }

  slides.forEach((slide, index) => {
    slide.hidden = false;
    slide.classList.toggle("is-active", index === 0);
    slide.setAttribute("aria-hidden", index === 0 ? "false" : "true");
  });

  if (slides.length < 2) return;

  function interactionPaused() {
    return rail.matches(":hover") || rail.contains(document.activeElement);
  }

  function clearTimer() {
    window.clearTimeout(timer);
    timer = null;
  }

  function schedule() {
    clearTimer();
    if (reducedMotion.matches || userPaused || interactionPaused() || document.hidden) return;
    timer = window.setTimeout(() => showSlide(current + 1, false), 6500);
  }

  function showSlide(index, manual) {
    const nextIndex = (index + slides.length) % slides.length;
    if (manual && !interactionHydrated) {
      hydrateAllSlides();
    } else {
      hydrateSlideAt(nextIndex);
    }
    slides.forEach((slide, slideIndex) => {
      const active = slideIndex === nextIndex;
      slide.classList.toggle("is-active", active);
      slide.setAttribute("aria-hidden", active ? "false" : "true");
    });
    dots.forEach((dot, dotIndex) => {
      if (dotIndex === nextIndex) {
        dot.setAttribute("aria-current", "true");
      } else {
        dot.removeAttribute("aria-current");
      }
    });
    current = nextIndex;
    if (currentNumber) currentNumber.textContent = String(current + 1);
    if (manual) clearTimer();
    schedule();
  }

  function updateMotionPreference() {
    rail.classList.toggle("is-reduced-motion", reducedMotion.matches);
    if (pause) pause.hidden = reducedMotion.matches;
    showSlide(current, false);
  }

  previous?.addEventListener("click", () => showSlide(current - 1, true));
  next?.addEventListener("click", () => showSlide(current + 1, true));
  dots.forEach((dot, index) =>
    dot.addEventListener("click", () => showSlide(index, true)),
  );

  pause?.addEventListener("click", () => {
    userPaused = !userPaused;
    pause.innerHTML = userPaused
      ? '<span aria-hidden="true">&#9654;</span>'
      : '<span aria-hidden="true">&#10074;&#10074;</span>';
    pause.setAttribute(
      "aria-label",
      userPaused ? "Start automatic photos" : "Pause automatic photos",
    );
    pause.setAttribute(
      "title",
      userPaused ? "Start automatic photos" : "Pause automatic photos",
    );
    schedule();
  });

  rail.addEventListener("mouseenter", clearTimer);
  rail.addEventListener("mouseleave", schedule);
  rail.addEventListener("focusin", clearTimer);
  rail.addEventListener("focusout", () => window.setTimeout(schedule, 0));
  document.addEventListener("visibilitychange", schedule);
  reducedMotion.addEventListener?.("change", updateMotionPreference);

  updateMotionPreference();
  window.setTimeout(() => hydrateSlideAt(current + 1), 5000);
});

function setupReadingProgress() {
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const progress = document.createElement("div");
  progress.className = "reading-progress";
  progress.setAttribute("aria-hidden", "true");
  document.body.prepend(progress);

  let ticking = false;

  function update() {
    const scrollTop = window.scrollY || document.documentElement.scrollTop || 0;
    const maxScroll = Math.max(
      1,
      document.documentElement.scrollHeight - window.innerHeight,
    );
    const ratio = Math.min(1, Math.max(0, scrollTop / maxScroll));
    document.documentElement.style.setProperty("--reading-progress", String(ratio));
    ticking = false;
  }

  function requestUpdate() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(update);
  }

  update();
  window.addEventListener("scroll", requestUpdate, { passive: true });
  window.addEventListener("resize", requestUpdate);
  reducedMotion.addEventListener?.("change", requestUpdate);
}

setupReadingProgress();
setupRevealMotion();


function setupSupportLinkTracking() {
  const storageKey = "lcaSupportEntry";
  document.addEventListener("click", (event) => {
    const link = event.target.closest?.('a[href]');
    if (!link) return;
    const url = new URL(link.href, window.location.origin);
    if (url.origin !== window.location.origin) return;
    if (url.pathname.replace(/\/$/, "") !== "/support-request") return;

    const payload = {
      ctaText: link.textContent.trim().replace(/\s+/g, " "),
      sourceTitle: document.title,
      sourceUrl: window.location.href,
      sourcePath: `${window.location.pathname}${window.location.search}${window.location.hash}`,
      targetUrl: `${url.pathname}${url.search}${url.hash}`,
      clickedAt: new Date().toISOString(),
    };

    try {
      window.sessionStorage.setItem(storageKey, JSON.stringify(payload));
    } catch (error) {
      // Session storage is optional; hidden form fields still fall back to document.referrer.
    }
  });
}

function setupSupportRequestMetadata() {
  const storageKey = "lcaSupportEntry";
  const params = new URLSearchParams(window.location.search);
  let stored = null;

  try {
    stored = JSON.parse(window.sessionStorage.getItem(storageKey) || "null");
  } catch (error) {
    stored = null;
  }

  function setValue(form, selector, value) {
    const field = form.querySelector(selector);
    if (field) field.value = value || "";
  }

  supportForms.forEach((form) => {
    const email = form.querySelector('#support-email, input[name="email"]');
    const replyTo = form.querySelector('[data-replyto-field]');
    const customerCopy = form.querySelector('[data-customer-copy-field]');
    const sourceUrl = stored?.sourceUrl || document.referrer || "Direct / unknown source";
    const sourcePath = stored?.sourcePath || (document.referrer ? new URL(document.referrer).pathname : "Direct / unknown path");
    const sourceCta = params.get("cta") || params.get("source") || stored?.ctaText || "Direct visit or untracked button";
    const note = [
      `Support form intake source: ${sourceCta}`,
      `Source page: ${sourcePath}`,
      `Source URL: ${sourceUrl}`,
      `Current URL: ${window.location.href}`,
    ].join(" | ");

    setValue(form, '[data-entry-source-url]', sourceUrl);
    setValue(form, '[data-entry-source-page]', sourcePath);
    setValue(form, '[data-entry-source-cta]', sourceCta);
    setValue(form, '[data-entry-source-note]', note);

    const needType = form.querySelector('#support-need-type');
    const message = form.querySelector('#support-issue');
    const topic = params.get("topic") || params.get("need_type");
    const messageText = params.get("message") || params.get("prefill");

    if (needType && topic) {
      Array.from(needType.options).some((option) => {
        if (option.textContent.trim().toLowerCase() === topic.trim().toLowerCase()) {
          needType.value = option.value;
          return true;
        }
        return false;
      });
    }

    if (message && messageText && !message.value) {
      message.value = messageText;
    }

    function syncEmailFields() {
      const value = email?.value?.trim() || "";
      if (replyTo) replyTo.value = value;
      if (customerCopy) customerCopy.value = value;
    }

    email?.addEventListener("input", syncEmailFields);
    form.addEventListener("submit", syncEmailFields, { capture: true });
    syncEmailFields();
  });
}

setupSupportLinkTracking();
setupSupportRequestMetadata();

function setupSupportSuccessModal() {
  const modal = document.querySelector("[data-support-success-modal]");
  if (!modal) return null;

  const panel = modal.querySelector(".support-success-modal__panel");
  const closeButtons = Array.from(modal.querySelectorAll("[data-support-success-close]"));
  const newRequestButton = modal.querySelector("[data-support-new-request]");
  const tailStatus = modal.querySelector("[data-support-tail-status]");
  let lastFocused = null;

  function normalizeTailNumber(value) {
    const cleaned = String(value || "").trim().replace(/\s+/g, " ").toUpperCase();
    return cleaned || "Aircraft";
  }

  function open(options = {}) {
    lastFocused = document.activeElement;
    if (tailStatus) {
      tailStatus.textContent = `${normalizeTailNumber(options.tailNumber)} is on the Board.`;
    }
    modal.hidden = false;
    modal.classList.add("is-open");
    document.body.classList.add("support-success-open");
    requestAnimationFrame(() => panel?.focus());
  }

  function close() {
    modal.classList.remove("is-open");
    document.body.classList.remove("support-success-open");
    modal.hidden = true;
    if (lastFocused && typeof lastFocused.focus === "function") {
      lastFocused.focus();
    }
  }

  closeButtons.forEach((button) => button.addEventListener("click", close));
  modal.addEventListener("click", (event) => {
    if (event.target === modal) close();
  });
  document.addEventListener("keydown", (event) => {
    if (!modal.classList.contains("is-open")) return;
    if (event.key === "Escape") close();
  });

  return { open, close, newRequestButton };
}


function setupSupportFailureModal() {
  const modal = document.querySelector("[data-support-failure-modal]");
  if (!modal) return null;

  const panel = modal.querySelector(".support-failure-modal__panel");
  const message = modal.querySelector("[data-support-failure-message]");
  const closeButtons = Array.from(modal.querySelectorAll("[data-support-failure-close]"));
  let lastFocused = null;

  function open(text) {
    lastFocused = document.activeElement;
    if (message && text) {
      message.innerHTML = `${text} Please call or text <strong>980.382.1344</strong> so the issue is not missed.`;
    }
    modal.hidden = false;
    modal.classList.add("is-open");
    document.body.classList.add("support-failure-open");
    requestAnimationFrame(() => panel?.focus());
  }

  function close() {
    modal.classList.remove("is-open");
    document.body.classList.remove("support-failure-open");
    modal.hidden = true;
    if (lastFocused && typeof lastFocused.focus === "function") {
      lastFocused.focus();
    }
  }

  closeButtons.forEach((button) => button.addEventListener("click", close));
  modal.addEventListener("click", (event) => {
    if (event.target === modal) close();
  });
  document.addEventListener("keydown", (event) => {
    if (!modal.classList.contains("is-open")) return;
    if (event.key === "Escape") close();
  });

  return { open, close };
}

// Keep support metadata synced for standard Formspree POST submissions.
// Do not intercept the submit event here. Form reliability is more important
// than custom AJAX success UI; the browser posts directly to Formspree.
supportForms.forEach((form) => {
  const email = form.querySelector('#support-email, input[name="email"]');
  const replyTo = form.querySelector('[data-replyto-field]');
  const customerCopy = form.querySelector('[data-customer-copy-field]');
  const submit = form.querySelector('button[type="submit"]');

  function syncEmailFields() {
    const value = email?.value?.trim() || "";
    if (replyTo) replyTo.value = value;
    if (customerCopy) customerCopy.value = value;
  }

  email?.addEventListener("input", syncEmailFields);
  form.addEventListener("submit", () => {
    syncEmailFields();
    if (submit) {
      submit.textContent = "Sending...";
      // Do not disable the button before native submission; some browsers can
      // drop submitter data when disabled during the submit event.
    }
  }, { capture: true });
  syncEmailFields();
});
