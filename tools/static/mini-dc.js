/*! mini-dc.js – kleiner Renderer für die Bekauri-Entwürfe (statische Fassung).
 * Unterstützt: {{pfad}}-Platzhalter in Text und Attributen, <sc-for>, <sc-if>,
 * onClick-Handler und setState() mit DOM-Abgleich. Keine Abhängigkeiten. */
(function () {
  'use strict';
  var HOLE = /\{\{\s*([^}]+?)\s*\}\}/g;
  var WHOLE = /^\s*\{\{\s*([^}]+?)\s*\}\}\s*$/;
  var HTML_NS = 'http://www.w3.org/1999/xhtml';

  function lookup(scope, expr) {
    expr = expr.trim();
    if (expr === 'true') return true;
    if (expr === 'false') return false;
    if (expr === 'null') return null;
    if (/^-?\d+(\.\d+)?$/.test(expr)) return Number(expr);
    if (/^(['"]).*\1$/.test(expr)) return expr.slice(1, -1);
    var parts = expr.split('.');
    var v = scope[parts[0]];
    for (var i = 1; i < parts.length; i++) {
      if (v == null) return undefined;
      v = v[parts[i]];
    }
    return v;
  }
  function str(v) { return v == null ? '' : String(v); }
  function interp(s, scope) {
    return s.replace(HOLE, function (_, e) { return str(lookup(scope, e)); });
  }
  function holeOf(el, attr) {
    var m = (el.getAttribute(attr) || '').match(WHOLE);
    return m ? m[1] : null;
  }

  function renderKids(node, scope, out) {
    var ch = node.childNodes;
    for (var i = 0; i < ch.length; i++) render(ch[i], scope, out);
  }

  function render(node, scope, out) {
    if (node.nodeType === 3) {
      out.push(document.createTextNode(node.data.indexOf('{{') < 0 ? node.data : interp(node.data, scope)));
      return;
    }
    if (node.nodeType !== 1) return;
    var tag = node.localName;
    if (tag === 'sc-for') {
      var list = lookup(scope, holeOf(node, 'list') || '') || [];
      var as = node.getAttribute('as') || 'item';
      for (var i = 0; i < list.length; i++) {
        var s = Object.create(scope);
        s[as] = list[i];
        s.$index = i;
        renderKids(node, s, out);
      }
      return;
    }
    if (tag === 'sc-if') {
      var cond = holeOf(node, 'value');
      if (cond && lookup(scope, cond)) renderKids(node, scope, out);
      return;
    }
    var ns = node.namespaceURI;
    var el = ns && ns !== HTML_NS ? document.createElementNS(ns, tag) : document.createElement(tag);
    var attrs = node.attributes;
    for (var j = 0; j < attrs.length; j++) {
      var a = attrs[j], name = a.name, val = a.value;
      if (name.indexOf('hint-') === 0) continue;
      var whole = val.match(WHOLE);
      if (name.slice(0, 2) === 'on') {
        var fn = whole ? lookup(scope, whole[1]) : null;
        if (typeof fn === 'function') (el.__h || (el.__h = {}))[name.slice(2)] = fn;
        continue;
      }
      var v = whole ? str(lookup(scope, whole[1])) : (val.indexOf('{{') < 0 ? val : interp(val, scope));
      if (a.namespaceURI) el.setAttributeNS(a.namespaceURI, name, v);
      else el.setAttribute(name, v);
    }
    var kids = [];
    renderKids(node, scope, kids);
    for (var k = 0; k < kids.length; k++) el.appendChild(kids[k]);
    out.push(el);
  }

  // Bestehendes DOM an das neu gerenderte angleichen (erhält Eingaben, Fokus, <details>-Zustand)
  function morph(parent, nodes) {
    for (var i = 0; i < nodes.length; i++) {
      var o = parent.childNodes[i], n = nodes[i];
      if (!o) { parent.appendChild(n); continue; }
      if (o.nodeType !== n.nodeType || o.nodeName !== n.nodeName) { parent.replaceChild(n, o); continue; }
      if (o.nodeType === 3) { if (o.data !== n.data) o.data = n.data; continue; }
      var oa = o.attributes, na = n.attributes, j;
      for (j = oa.length - 1; j >= 0; j--) {
        var nm = oa[j].name;
        if (!n.hasAttribute(nm) && !(nm === 'open' && o.localName === 'details')) o.removeAttribute(nm);
      }
      for (j = 0; j < na.length; j++) {
        if (o.getAttribute(na[j].name) !== na[j].value) o.setAttribute(na[j].name, na[j].value);
      }
      o.__h = n.__h;
      morph(o, Array.prototype.slice.call(n.childNodes));
    }
    while (parent.childNodes.length > nodes.length) parent.removeChild(parent.lastChild);
  }

  ['click', 'input', 'change', 'submit', 'keydown'].forEach(function (type) {
    document.addEventListener(type, function (e) {
      var el = e.target;
      while (el && el !== document) {
        if (el.__h && el.__h[type]) { el.__h[type](e); return; }
        el = el.parentNode;
      }
    });
  });

  function DCLogic(props) { this.props = props || {}; this.state = {}; }
  DCLogic.prototype.setState = function (p) {
    Object.assign(this.state, typeof p === 'function' ? p(this.state, this.props) : p);
    if (this.__schedule) this.__schedule();
  };
  DCLogic.prototype.forceUpdate = function () { if (this.__schedule) this.__schedule(); };
  window.DCLogic = DCLogic;

  window.MiniDC = {
    mount: function (C, props) {
      var tpl = document.getElementById('dc-template');
      var root = document.getElementById('app');
      var inst = new C(props || {});
      var pending = false;
      function draw() {
        pending = false;
        var vals = inst.renderVals ? inst.renderVals() : {};
        var out = [];
        renderKids(tpl.content, vals, out);
        morph(root, out);
      }
      inst.__schedule = function () {
        if (!pending) { pending = true; Promise.resolve().then(draw); }
      };
      draw();
      if (inst.componentDidMount) inst.componentDidMount();
      return inst;
    }
  };
})();
