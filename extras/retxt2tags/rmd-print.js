/* This script is a companion to remarkdown.css, by fvsch.com
   License: Do What The Fuck You Want To Public License (WTFPL), Version 2
   http://fvsch.com/code/css/remarkdown/COPYING */

(function(){
/*  Generates a list of link URLs at the end of each element
 *  sporting a "rmd-print" class.
 */
var blocks = document.querySelectorAll('.rmd-a-printref');
var count  = 1; // reference count is global to the document

for (var iB=0, maxB=blocks.length; iB<maxB; iB++) {
  var block = blocks[iB];
  var links = block.getElementsByTagName('A');
  var list  = document.createElement('OL');
  list.className = 'rmd-references';
  list.setAttribute('start', count);

  for (var iL=0, maxL=links.length; iL<maxL; iL++) {
    var link = links[iL];
    var text = link.textContent || link.innerText;
    var url  = link.href;
    var href = link.getAttribute('href', 2);
     // Exclude this link if internal, or already counted, or a simple mailto
    if (/^#/.test(href) || link.getAttribute('data-rmd-linkref')) {continue}
    if (/^mailto/.test(href)) {
      var email = href.replace(/^\s*mailto\s*:\s*|\s*$/g,'');
      if (text.indexOf(email) == -1) { url = email }
      else { continue }
    }
    // Add reference number to link as a custom attribute
    link.setAttribute('data-rmd-linkref', count);
    // Create list item showing URL as plain text
    var item = document.createElement('LI');
    item.setAttribute('data-rmd-linknum', count);
    item.innerHTML = url;
    list.appendChild(item);
    count++;
  }
  block.appendChild(list);
}

})();

