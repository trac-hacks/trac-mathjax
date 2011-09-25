MathJax.Hub.Config({'tex2jax': {
  // We should disable both inline and display parsing and leave to Trac to
  // possibly (in future versions) parse original source, but currently it
  // seems it is impossible to do so, so we set it to something not so common
  'inlineMath': [['[tex]', '[/tex]']],
  'displayMath': [['[blocktex]', '[/blocktex]']],
  'processEnvironments': false
}});

MathJax.Hub.Configured();
