Vue.component('frag', {
  props: ['nref'],
  template: `
    <div class="text">
      <div class="ref">{{ passageRef }}</div>
      <span v-for="line in lines">
        <span class="line">{{ line[0].split('.')[1] }}</span>
        <span v-for="(token, index) in line[1].split(' ')" :class="{ selected: highlight(line, index)}">{{ token }}</span>
        <br>
      </span>
    </div>
  `,
  data() {
    return {
      lines: null,
    }
  },
  computed: {
    passageRef() {
      const work = 'Il.'
      const [startBook, startLine, startOffset, endBook, endLine, endOffset] = this.nref;
      if (startBook == endBook && startLine == endLine) {
        return `${work} ${startBook}.${startLine}`;
      }
      else if (startBook == endBook) {
        return `${work} ${startBook}.${startLine}–${endLine}`;
      }
      else {
        return `${work} ${startBook}.${startLine}–${endBook}.${endLine}`;
      }
    },
    urn() {
      const work = 'Il.'
      const [startBook, startLine, startOffset, endBook, endLine, endOffset] = this.nref;
      const ctsWork = {
        'Il.': 'tlg0012.tlg001.perseus-grc2',
        // 'Od': 'tlg0012.tlg002.perseus-grc2',
      }[work]
      firstLine = Math.max(Number(startLine) - 3, 1);
      lastLine = Math.min(Number(endLine) + 3, 1000);  // @@@ sub 1000 with book length
      return `urn:cts:greekLit:${ctsWork}:${startBook}.${firstLine}-${endBook}.${lastLine}`;
    }
  },
  created() {
    const apiUrl = `https://homer-api.herokuapp.com/${this.urn}/`;
    axios.get(apiUrl).then(response => {
      this.lines = response.data
    });
  },
  methods: {
    highlight(line, index) {
      const [startBook, startLine, startOffset, endBook, endLine, endOffset] = this.nref;
      const [currBook, currLine] = line[0].split('.');
      // @@@ assume startBook == currBook == endBook for now
      if (currLine < startLine) return false;
      if (currLine > endLine) return false;
      if (startLine < currLine && currLine < endLine) return true;
      if (startLine == currLine && Math.round(1000 * index / line[1].split(' ').length) < startOffset) return false;
      if (endLine == currLine && Math.round(1000 * index / line[1].split(' ').length) >= endOffset) return false;
      return true;
    },
  },
});

var app = new Vue({
  el: '#app',
  computed: {
    ngramContent() {
      return ngramData[this.ngramId - 1][0];
    },
    ngramRefs() {
      return ngramData[this.ngramId - 1][1];
    }
  },
  created() {
    // @@@ until we introduce vue-router
    const params = new URLSearchParams(window.location.search.substring(1));
    const ngramId = Number(params.get("ngram"));
    if (ngramId) {
      if (ngramId >= ngramData.length) {
        this.ngramId = ngramData.length - 1;
      }
      else {
        this.ngramId = ngramId;
      }
    }
    else {
      this.ngramId = 315;
    }
  }
});
