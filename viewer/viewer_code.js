Display = function() {
  this.draw = SVG('drawing').size(1200, 1000);

  this.width = 50;  // width of book (including gutter)
  this.gutter = 5;  // space between books
  this.top_margin = 20;  // space at top before book begins

}
Display.prototype = {

  drawLine: function(book, line, start_offset, end_offset, ngram_id, ngram_length) {
    // offsets range from 0 (start of line) to 1000 (end of line)

    var y = this.top_margin + (line - 1);
    var sx = (book - 1) * this.width + start_offset * (this.width - this.gutter) / 1000;
    var ex = (book - 1) * this.width + end_offset * (this.width - this.gutter) / 1000;

    this.draw.line(sx, y, ex, y)
      .stroke({ width: 1})
      .addClass('nlength-' + ngram_length)
      .addClass('ngram-' + ngram_id)
      .addClass('ngram');
  },

  drawBooks: function(book_lengths) {
    for (var i = 0; i < book_lengths.length; i++) {
      var l = book_lengths[i];
      this.draw.text((i + 1).toString())
        .move((i + 0.5) * this.width - (this.gutter / 2), 0)
        .attr({ stroke: '#CCC'})
        .font('anchor', 'middle');
      this.draw.rect(this.width - this.gutter, l)
        .move(i * this.width, this.top_margin - 0.5)
        .attr({ fill: '#F0F0F0'});
    }
  },

  drawNGrams: function(ngram_offsets) {
    for (var i = 0; i < ngram_offsets.length; i++) {

      var n = ngram_offsets[i];

      var ngram_id = n[0];
      var ngram_length = n[1];
      var start_book = n[2];
      var start_line = n[3];
      var start_offset = n[4];
      var end_book = n[5];
      var end_line = n[6];
      var end_offset = n[7];

      for (var line = start_line; line <= end_line; line++) {
        this.drawLine(start_book, line,
          line === start_line ? start_offset : 0,
          line === end_line ? end_offset : 1000,
          ngram_id, ngram_length
        );
      }

    }
  }
}

var display = new Display();
display.drawBooks(book_lengths);
display.drawNGrams(ngram_offsets);
