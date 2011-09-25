jQuery(document).ready(function ($) {
  $(document).ajaxSuccess(function () {
    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
  });
});
