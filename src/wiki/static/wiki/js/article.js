$(document).ready(function() {

  $('.wiki-article .article-list ul, .wiki-article .toc ul').each(function() {
    $(this).addClass('nav');
    $(this).addClass('nav-list');
  });
  var wiki_article = document.querySelector(".wiki-article")
  var matches = wiki_article.querySelectorAll("a");

  for (var i = 0; i < matches.length; i++){
    // matches[i].href.toString().includes("wiki")
    if (!matches[i].href.toString().includes("wiki") || matches[i].href.toString().includes("sixcycle-wiki-storage.s3.amazonaws.com")) {
     matches[i].setAttribute('target', '_blank');
    }
  }
});
