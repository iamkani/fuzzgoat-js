const asciidoctor = require('asciidoctor')()

function fuzz(buf) {
	asciidoctor.convert(Buffer.from('103a3a0a393e0901', 'hex'))
}

module.exports = {
    fuzz
};
