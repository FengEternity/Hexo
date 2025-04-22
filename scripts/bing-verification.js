hexo.extend.generator.register('bing-verification', function(locals) {
  return {
    path: 'BingSiteAuth.xml',
    data: '<?xml version="1.0"?>\n<users>\n\t<user>6148858196500BD634907AE54A6CE9EB</user>\n</users>'
  };
});
