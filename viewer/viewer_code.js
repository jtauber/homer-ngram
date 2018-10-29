Display = function() {

  this.draw = SVG('drawing').size(1200, 1000);

  this.width = 50;  // width of book (including gutter)
  this.gutter = 5;  // space between books
  this.top_margin = 20;  // space at top before book begins

}
Display.prototype = {

  drawLine: function(book, line, start_offset, end_offset, ngram_id, ngram_length) {

    // offsets range from 0 (start of line) to 1000 (end of line)

    var book_start = (book - 1) * this.width;
    var book_width = (this.width - this.gutter) / 1000;

    var y = this.top_margin + (line - 1);
    var sx = book_start + start_offset * book_width;
    var ex = book_start + end_offset * book_width;

    this.draw.line(sx, y, ex, y)
      .stroke({ width: 1})
      .addClass('ngram')
      // the next two are just in case we want to style by length or id
      .addClass('nlength-' + ngram_length)
      .addClass('ngram-' + ngram_id);

  },

  drawBooks: function(book_lengths) {

    // iterate over books to get lengths

    for (var i = 0; i < book_lengths.length; i++) {

      // get the length of the (i+1)-th book
      var l = book_lengths[i];

      this.draw.text((i + 1).toString())
        .move((i + 0.5) * this.width - (this.gutter / 2), 0)
        .addClass('book-num');

      this.draw.rect(this.width - this.gutter, l)
        .move(i * this.width, this.top_margin - 0.5)
        .addClass('book');

    }

  },

  drawNGrams: function(ngram_offsets) {

    // iterate over n-grams to get offset data

    for (var i = 0; i < ngram_offsets.length; i++) {

      // get the i-th n-gram
      var n = ngram_offsets[i];

      // break out the properties for this ngram
      var ngram_id = n[0];
      var ngram_length = n[1];
      var start_book = n[2];
      var start_line = n[3];
      var start_offset = n[4];
      var end_book = n[5];
      var end_line = n[6];
      var end_offset = n[7];

      // iterate over all the lines (possibly just one) in n-gram
      for (var line = start_line; line <= end_line; line++) {
        this.drawLine(start_book, line,
          // only use start_offset on first line, otherwise 0
          line == start_line ? start_offset : 0,
          // only use end_offset on last line, otherwise 1000
          line == end_line ? end_offset : 1000,
          ngram_id, ngram_length
        );
      }

    }
  }
}

var display = new Display();

display.drawBooks(book_lengths);
display.drawNGrams(ngram_offsets);
