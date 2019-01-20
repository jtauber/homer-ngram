Vue.component('frag', {
  props: ['nref'],
  template: `
    <div class="text">
      <div class="ref">{{ nref }}</div>
      <span v-for="line in lines">
        <span class="line">{{ line[0].split('.')[1] }}</span>
        <span :class="{ selected: line[0] == shortRef }">{{ line[1] }}</span>
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
    shortRef() {
      return this.nref.split('.').slice(1).join('.');
    },
    urn () {
      const [work, book, line] = this.nref.split('.');
      const ctsWork = {
        'Il': 'tlg0012.tlg001.perseus-grc2',
        // 'Od': 'tlg0012.tlg002.perseus-grc2',
      }[work]
      startLine = Math.max(Number(line) - 3, 1);
      endLine = Math.min(Number(line) + 3, 1000);  // @@@ sub 1000 with book length
      return `urn:cts:greekLit:${ctsWork}:${book}.${startLine}-${book}.${endLine}`;
    }
  },
  created() {
    const apiUrl = `http://localhost:5000/${this.urn}/`;
    axios.get(apiUrl).then(response => {
      this.lines = response.data
    });
  }
});

var app = new Vue({
  el: '#app',
  data: {
    ngramId: '315',
    ngramContent: 'τὸν δʼ ἄρʼ ὑπόδρα ἰδὼν προσέφη πόδας ὠκὺς Ἀχιλλεύς',
    ngramRefs: [
      'Il.1.148',
      'Il.22.260',
      'Il.24.559',
    ],
  },
});
