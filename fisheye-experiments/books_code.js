Display = function() {

  this.draw = SVG('drawing').size(1250, 1000);

  this.width = 50;  // width of book (including gutter)
  this.gutter = 5;  // space between books
  this.top_margin = 20;  // space at top before book begins

  this.zoom = 3;  // how much the width of a book is zoomed on hover
  this.duration = 50; // millisecond duration of book width animation

}
Display.prototype = {

  drawBooks: function(book_lengths) {

    this.book_labels = [];
    this.book_rects = [];

    // iterate over books to get lengths

    for (var i = 0; i < book_lengths.length; i++) {

      // get the length of the (i+1)-th book
      var l = book_lengths[i];

      this.book_labels[i] = this.draw.text((i + 1).toString())
        .move((i + 0.5) * this.width - (this.gutter / 2), 0)
        .addClass('book-num');

      var d = this;

      this.book_rects[i] = this.draw.rect(this.width - this.gutter, l)
        .move(i * this.width, this.top_margin - 0.5)
        .data('num', i)
        .addClass('book')
        .on('mouseover', function() {
          for (var j = 0; j < book_lengths.length; j++) {
            if (j < this.data('num')) {
              d.book_rects[j]
                .animate(d.duration)
                .move(j * d.width, d.top_margin - 0.5)
                .width(d.width - d.gutter);
              d.book_labels[j]
                .animate(d.duration)
                .move((j + 0.5) * d.width - (d.gutter / 2), 0)
            } else if (j == this.data('num')) {
              d.book_rects[j]
                .animate(d.duration)
                .move(j * d.width, d.top_margin - 0.5)
                .width(d.zoom * d.width - d.gutter);
              d.book_labels[j]
                .animate(d.duration)
                .move(j * d.width + (0.5 * d.width * d.zoom) - (d.gutter / 2), 0)
            } else if (j > this.data('num')) {
              d.book_rects[j]
                .animate(d.duration)
                .move((j + (d.zoom - 1)) * d.width, d.top_margin - 0.5)
                .width(d.width - d.gutter);
              d.book_labels[j]
                .animate(d.duration)
                .move((j + (d.zoom - 1) + 0.5) * d.width - (d.gutter / 2), 0)
            }
          }
        });
    }
  }
}

var display = new Display();

display.drawBooks(book_lengths);
