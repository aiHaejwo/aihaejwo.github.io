document.addEventListener("DOMContentLoaded", () => {
  const header = document.getElementById("site-header");
  const updateHeader = () => header.classList.toggle("is-scrolled", window.scrollY > 16);

  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });

  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.12 }
  );

  document.querySelectorAll("[data-reveal]").forEach((element) => revealObserver.observe(element));
});
