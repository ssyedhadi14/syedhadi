var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });
var __esm = (fn, res, err) => function __init() {
  if (err) throw err[0];
  try {
    return fn && (res = (0, fn[__getOwnPropNames(fn)[0]])(fn = 0)), res;
  } catch (e) {
    throw err = [e], e;
  }
};
var __commonJS = (cb, mod3) => function __require() {
  try {
    return mod3 || (0, cb[__getOwnPropNames(cb)[0]])((mod3 = { exports: {} }).exports, mod3), mod3.exports;
  } catch (e) {
    throw mod3 = 0, e;
  }
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod3, isNodeMode, target) => (target = mod3 != null ? __create(__getProtoOf(mod3)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod3 || !mod3.__esModule ? __defProp(target, "default", { value: mod3, enumerable: true }) : target,
  mod3
));

// ../../wr/node_modules/unenv/dist/runtime/_internal/utils.mjs
// @__NO_SIDE_EFFECTS__
function createNotImplementedError(name) {
  return new Error(`[unenv] ${name} is not implemented yet!`);
}
// @__NO_SIDE_EFFECTS__
function notImplemented(name) {
  const fn = /* @__PURE__ */ __name(() => {
    throw /* @__PURE__ */ createNotImplementedError(name);
  }, "fn");
  return Object.assign(fn, { __unenv__: true });
}
// @__NO_SIDE_EFFECTS__
function notImplementedClass(name) {
  return class {
    __unenv__ = true;
    constructor() {
      throw new Error(`[unenv] ${name} is not implemented yet!`);
    }
  };
}
var init_utils = __esm({
  "../../wr/node_modules/unenv/dist/runtime/_internal/utils.mjs"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    __name(createNotImplementedError, "createNotImplementedError");
    __name(notImplemented, "notImplemented");
    __name(notImplementedClass, "notImplementedClass");
  }
});

// ../../wr/node_modules/unenv/dist/runtime/node/internal/perf_hooks/performance.mjs
var _timeOrigin, _performanceNow, nodeTiming, PerformanceEntry, PerformanceMark, PerformanceMeasure, PerformanceResourceTiming, PerformanceObserverEntryList, Performance, PerformanceObserver, performance;
var init_performance = __esm({
  "../../wr/node_modules/unenv/dist/runtime/node/internal/perf_hooks/performance.mjs"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    init_utils();
    _timeOrigin = globalThis.performance?.timeOrigin ?? Date.now();
    _performanceNow = globalThis.performance?.now ? globalThis.performance.now.bind(globalThis.performance) : () => Date.now() - _timeOrigin;
    nodeTiming = {
      name: "node",
      entryType: "node",
      startTime: 0,
      duration: 0,
      nodeStart: 0,
      v8Start: 0,
      bootstrapComplete: 0,
      environment: 0,
      loopStart: 0,
      loopExit: 0,
      idleTime: 0,
      uvMetricsInfo: {
        loopCount: 0,
        events: 0,
        eventsWaiting: 0
      },
      detail: void 0,
      toJSON() {
        return this;
      }
    };
    PerformanceEntry = class {
      static {
        __name(this, "PerformanceEntry");
      }
      __unenv__ = true;
      detail;
      entryType = "event";
      name;
      startTime;
      constructor(name, options) {
        this.name = name;
        this.startTime = options?.startTime || _performanceNow();
        this.detail = options?.detail;
      }
      get duration() {
        return _performanceNow() - this.startTime;
      }
      toJSON() {
        return {
          name: this.name,
          entryType: this.entryType,
          startTime: this.startTime,
          duration: this.duration,
          detail: this.detail
        };
      }
    };
    PerformanceMark = class PerformanceMark2 extends PerformanceEntry {
      static {
        __name(this, "PerformanceMark");
      }
      entryType = "mark";
      constructor() {
        super(...arguments);
      }
      get duration() {
        return 0;
      }
    };
    PerformanceMeasure = class extends PerformanceEntry {
      static {
        __name(this, "PerformanceMeasure");
      }
      entryType = "measure";
    };
    PerformanceResourceTiming = class extends PerformanceEntry {
      static {
        __name(this, "PerformanceResourceTiming");
      }
      entryType = "resource";
      serverTiming = [];
      connectEnd = 0;
      connectStart = 0;
      decodedBodySize = 0;
      domainLookupEnd = 0;
      domainLookupStart = 0;
      encodedBodySize = 0;
      fetchStart = 0;
      initiatorType = "";
      name = "";
      nextHopProtocol = "";
      redirectEnd = 0;
      redirectStart = 0;
      requestStart = 0;
      responseEnd = 0;
      responseStart = 0;
      secureConnectionStart = 0;
      startTime = 0;
      transferSize = 0;
      workerStart = 0;
      responseStatus = 0;
    };
    PerformanceObserverEntryList = class {
      static {
        __name(this, "PerformanceObserverEntryList");
      }
      __unenv__ = true;
      getEntries() {
        return [];
      }
      getEntriesByName(_name, _type) {
        return [];
      }
      getEntriesByType(type) {
        return [];
      }
    };
    Performance = class {
      static {
        __name(this, "Performance");
      }
      __unenv__ = true;
      timeOrigin = _timeOrigin;
      eventCounts = /* @__PURE__ */ new Map();
      _entries = [];
      _resourceTimingBufferSize = 0;
      navigation = void 0;
      timing = void 0;
      timerify(_fn, _options) {
        throw createNotImplementedError("Performance.timerify");
      }
      get nodeTiming() {
        return nodeTiming;
      }
      eventLoopUtilization() {
        return {};
      }
      markResourceTiming() {
        return new PerformanceResourceTiming("");
      }
      onresourcetimingbufferfull = null;
      now() {
        if (this.timeOrigin === _timeOrigin) {
          return _performanceNow();
        }
        return Date.now() - this.timeOrigin;
      }
      clearMarks(markName) {
        this._entries = markName ? this._entries.filter((e) => e.name !== markName) : this._entries.filter((e) => e.entryType !== "mark");
      }
      clearMeasures(measureName) {
        this._entries = measureName ? this._entries.filter((e) => e.name !== measureName) : this._entries.filter((e) => e.entryType !== "measure");
      }
      clearResourceTimings() {
        this._entries = this._entries.filter((e) => e.entryType !== "resource" || e.entryType !== "navigation");
      }
      getEntries() {
        return this._entries;
      }
      getEntriesByName(name, type) {
        return this._entries.filter((e) => e.name === name && (!type || e.entryType === type));
      }
      getEntriesByType(type) {
        return this._entries.filter((e) => e.entryType === type);
      }
      mark(name, options) {
        const entry = new PerformanceMark(name, options);
        this._entries.push(entry);
        return entry;
      }
      measure(measureName, startOrMeasureOptions, endMark) {
        let start2;
        let end;
        if (typeof startOrMeasureOptions === "string") {
          start2 = this.getEntriesByName(startOrMeasureOptions, "mark")[0]?.startTime;
          end = this.getEntriesByName(endMark, "mark")[0]?.startTime;
        } else {
          start2 = Number.parseFloat(startOrMeasureOptions?.start) || this.now();
          end = Number.parseFloat(startOrMeasureOptions?.end) || this.now();
        }
        const entry = new PerformanceMeasure(measureName, {
          startTime: start2,
          detail: {
            start: start2,
            end
          }
        });
        this._entries.push(entry);
        return entry;
      }
      setResourceTimingBufferSize(maxSize) {
        this._resourceTimingBufferSize = maxSize;
      }
      addEventListener(type, listener, options) {
        throw createNotImplementedError("Performance.addEventListener");
      }
      removeEventListener(type, listener, options) {
        throw createNotImplementedError("Performance.removeEventListener");
      }
      dispatchEvent(event) {
        throw createNotImplementedError("Performance.dispatchEvent");
      }
      toJSON() {
        return this;
      }
    };
    PerformanceObserver = class {
      static {
        __name(this, "PerformanceObserver");
      }
      __unenv__ = true;
      static supportedEntryTypes = [];
      _callback = null;
      constructor(callback) {
        this._callback = callback;
      }
      takeRecords() {
        return [];
      }
      disconnect() {
        throw createNotImplementedError("PerformanceObserver.disconnect");
      }
      observe(options) {
        throw createNotImplementedError("PerformanceObserver.observe");
      }
      bind(fn) {
        return fn;
      }
      runInAsyncScope(fn, thisArg, ...args) {
        return fn.call(thisArg, ...args);
      }
      asyncId() {
        return 0;
      }
      triggerAsyncId() {
        return 0;
      }
      emitDestroy() {
        return this;
      }
    };
    performance = globalThis.performance && "addEventListener" in globalThis.performance ? globalThis.performance : new Performance();
  }
});

// ../../wr/node_modules/unenv/dist/runtime/node/perf_hooks.mjs
var init_perf_hooks = __esm({
  "../../wr/node_modules/unenv/dist/runtime/node/perf_hooks.mjs"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    init_performance();
  }
});

// ../../wr/node_modules/@cloudflare/unenv-preset/dist/runtime/polyfill/performance.mjs
var init_performance2 = __esm({
  "../../wr/node_modules/@cloudflare/unenv-preset/dist/runtime/polyfill/performance.mjs"() {
    init_perf_hooks();
    if (!("__unenv__" in performance)) {
      const proto = Performance.prototype;
      for (const key of Object.getOwnPropertyNames(proto)) {
        if (key !== "constructor" && !(key in performance)) {
          const desc = Object.getOwnPropertyDescriptor(proto, key);
          if (desc) {
            Object.defineProperty(performance, key, desc);
          }
        }
      }
    }
    globalThis.performance = performance;
    globalThis.Performance = Performance;
    globalThis.PerformanceEntry = PerformanceEntry;
    globalThis.PerformanceMark = PerformanceMark;
    globalThis.PerformanceMeasure = PerformanceMeasure;
    globalThis.PerformanceObserver = PerformanceObserver;
    globalThis.PerformanceObserverEntryList = PerformanceObserverEntryList;
    globalThis.PerformanceResourceTiming = PerformanceResourceTiming;
  }
});

// ../../wr/node_modules/unenv/dist/runtime/mock/noop.mjs
var noop_default;
var init_noop = __esm({
  "../../wr/node_modules/unenv/dist/runtime/mock/noop.mjs"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    noop_default = Object.assign(() => {
    }, { __unenv__: true });
  }
});

// ../../wr/node_modules/unenv/dist/runtime/node/console.mjs
import { Writable } from "node:stream";
var _console, _ignoreErrors, _stderr, _stdout, log, info, trace, debug, table, error, warn, createTask, clear, count, countReset, dir, dirxml, group, groupEnd, groupCollapsed, profile, profileEnd, time, timeEnd, timeLog, timeStamp, Console, _times, _stdoutErrorHandler, _stderrErrorHandler;
var init_console = __esm({
  "../../wr/node_modules/unenv/dist/runtime/node/console.mjs"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    init_noop();
    init_utils();
    _console = globalThis.console;
    _ignoreErrors = true;
    _stderr = new Writable();
    _stdout = new Writable();
    log = _console?.log ?? noop_default;
    info = _console?.info ?? log;
    trace = _console?.trace ?? info;
    debug = _console?.debug ?? log;
    table = _console?.table ?? log;
    error = _console?.error ?? log;
    warn = _console?.warn ?? error;
    createTask = _console?.createTask ?? /* @__PURE__ */ notImplemented("console.createTask");
    clear = _console?.clear ?? noop_default;
    count = _console?.count ?? noop_default;
    countReset = _console?.countReset ?? noop_default;
    dir = _console?.dir ?? noop_default;
    dirxml = _console?.dirxml ?? noop_default;
    group = _console?.group ?? noop_default;
    groupEnd = _console?.groupEnd ?? noop_default;
    groupCollapsed = _console?.groupCollapsed ?? noop_default;
    profile = _console?.profile ?? noop_default;
    profileEnd = _console?.profileEnd ?? noop_default;
    time = _console?.time ?? noop_default;
    timeEnd = _console?.timeEnd ?? noop_default;
    timeLog = _console?.timeLog ?? noop_default;
    timeStamp = _console?.timeStamp ?? noop_default;
    Console = _console?.Console ?? /* @__PURE__ */ notImplementedClass("console.Console");
    _times = /* @__PURE__ */ new Map();
    _stdoutErrorHandler = noop_default;
    _stderrErrorHandler = noop_default;
  }
});

// ../../wr/node_modules/@cloudflare/unenv-preset/dist/runtime/node/console.mjs
var workerdConsole, assert, clear2, context, count2, countReset2, createTask2, debug2, dir2, dirxml2, error2, group2, groupCollapsed2, groupEnd2, info2, log2, profile2, profileEnd2, table2, time2, timeEnd2, timeLog2, timeStamp2, trace2, warn2, console_default;
var init_console2 = __esm({
  "../../wr/node_modules/@cloudflare/unenv-preset/dist/runtime/node/console.mjs"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    init_console();
    workerdConsole = globalThis["console"];
    ({
      assert,
      clear: clear2,
      context: (
        // @ts-expect-error undocumented public API
        context
      ),
      count: count2,
      countReset: countReset2,
      createTask: (
        // @ts-expect-error undocumented public API
        createTask2
      ),
      debug: debug2,
      dir: dir2,
      dirxml: dirxml2,
      error: error2,
      group: group2,
      groupCollapsed: groupCollapsed2,
      groupEnd: groupEnd2,
      info: info2,
      log: log2,
      profile: profile2,
      profileEnd: profileEnd2,
      table: table2,
      time: time2,
      timeEnd: timeEnd2,
      timeLog: timeLog2,
      timeStamp: timeStamp2,
      trace: trace2,
      warn: warn2
    } = workerdConsole);
    Object.assign(workerdConsole, {
      Console,
      _ignoreErrors,
      _stderr,
      _stderrErrorHandler,
      _stdout,
      _stdoutErrorHandler,
      _times
    });
    console_default = workerdConsole;
  }
});

// ../../wr/node_modules/wrangler/_virtual_unenv_global_polyfill-@cloudflare-unenv-preset-node-console
var init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console = __esm({
  "../../wr/node_modules/wrangler/_virtual_unenv_global_polyfill-@cloudflare-unenv-preset-node-console"() {
    init_console2();
    globalThis.console = console_default;
  }
});

// ../../wr/node_modules/unenv/dist/runtime/node/internal/process/hrtime.mjs
var hrtime;
var init_hrtime = __esm({
  "../../wr/node_modules/unenv/dist/runtime/node/internal/process/hrtime.mjs"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    hrtime = /* @__PURE__ */ Object.assign(/* @__PURE__ */ __name(function hrtime2(startTime) {
      const now = Date.now();
      const seconds = Math.trunc(now / 1e3);
      const nanos = now % 1e3 * 1e6;
      if (startTime) {
        let diffSeconds = seconds - startTime[0];
        let diffNanos = nanos - startTime[0];
        if (diffNanos < 0) {
          diffSeconds = diffSeconds - 1;
          diffNanos = 1e9 + diffNanos;
        }
        return [diffSeconds, diffNanos];
      }
      return [seconds, nanos];
    }, "hrtime"), { bigint: /* @__PURE__ */ __name(function bigint() {
      return BigInt(Date.now() * 1e6);
    }, "bigint") });
  }
});

// ../../wr/node_modules/unenv/dist/runtime/node/internal/tty/read-stream.mjs
var ReadStream;
var init_read_stream = __esm({
  "../../wr/node_modules/unenv/dist/runtime/node/internal/tty/read-stream.mjs"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    ReadStream = class {
      static {
        __name(this, "ReadStream");
      }
      fd;
      isRaw = false;
      isTTY = false;
      constructor(fd) {
        this.fd = fd;
      }
      setRawMode(mode) {
        this.isRaw = mode;
        return this;
      }
    };
  }
});

// ../../wr/node_modules/unenv/dist/runtime/node/internal/tty/write-stream.mjs
var WriteStream;
var init_write_stream = __esm({
  "../../wr/node_modules/unenv/dist/runtime/node/internal/tty/write-stream.mjs"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    WriteStream = class {
      static {
        __name(this, "WriteStream");
      }
      fd;
      columns = 80;
      rows = 24;
      isTTY = false;
      constructor(fd) {
        this.fd = fd;
      }
      clearLine(dir3, callback) {
        callback && callback();
        return false;
      }
      clearScreenDown(callback) {
        callback && callback();
        return false;
      }
      cursorTo(x, y, callback) {
        callback && typeof callback === "function" && callback();
        return false;
      }
      moveCursor(dx, dy, callback) {
        callback && callback();
        return false;
      }
      getColorDepth(env2) {
        return 1;
      }
      hasColors(count3, env2) {
        return false;
      }
      getWindowSize() {
        return [this.columns, this.rows];
      }
      write(str, encoding, cb) {
        if (str instanceof Uint8Array) {
          str = new TextDecoder().decode(str);
        }
        try {
          console.log(str);
        } catch {
        }
        cb && typeof cb === "function" && cb();
        return false;
      }
    };
  }
});

// ../../wr/node_modules/unenv/dist/runtime/node/tty.mjs
var init_tty = __esm({
  "../../wr/node_modules/unenv/dist/runtime/node/tty.mjs"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    init_read_stream();
    init_write_stream();
  }
});

// ../../wr/node_modules/unenv/dist/runtime/node/internal/process/node-version.mjs
var NODE_VERSION;
var init_node_version = __esm({
  "../../wr/node_modules/unenv/dist/runtime/node/internal/process/node-version.mjs"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    NODE_VERSION = "22.14.0";
  }
});

// ../../wr/node_modules/unenv/dist/runtime/node/internal/process/process.mjs
import { EventEmitter } from "node:events";
var Process;
var init_process = __esm({
  "../../wr/node_modules/unenv/dist/runtime/node/internal/process/process.mjs"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    init_tty();
    init_utils();
    init_node_version();
    Process = class _Process extends EventEmitter {
      static {
        __name(this, "Process");
      }
      env;
      hrtime;
      nextTick;
      constructor(impl) {
        super();
        this.env = impl.env;
        this.hrtime = impl.hrtime;
        this.nextTick = impl.nextTick;
        for (const prop of [...Object.getOwnPropertyNames(_Process.prototype), ...Object.getOwnPropertyNames(EventEmitter.prototype)]) {
          const value = this[prop];
          if (typeof value === "function") {
            this[prop] = value.bind(this);
          }
        }
      }
      // --- event emitter ---
      emitWarning(warning, type, code) {
        console.warn(`${code ? `[${code}] ` : ""}${type ? `${type}: ` : ""}${warning}`);
      }
      emit(...args) {
        return super.emit(...args);
      }
      listeners(eventName) {
        return super.listeners(eventName);
      }
      // --- stdio (lazy initializers) ---
      #stdin;
      #stdout;
      #stderr;
      get stdin() {
        return this.#stdin ??= new ReadStream(0);
      }
      get stdout() {
        return this.#stdout ??= new WriteStream(1);
      }
      get stderr() {
        return this.#stderr ??= new WriteStream(2);
      }
      // --- cwd ---
      #cwd = "/";
      chdir(cwd2) {
        this.#cwd = cwd2;
      }
      cwd() {
        return this.#cwd;
      }
      // --- dummy props and getters ---
      arch = "";
      platform = "";
      argv = [];
      argv0 = "";
      execArgv = [];
      execPath = "";
      title = "";
      pid = 200;
      ppid = 100;
      get version() {
        return `v${NODE_VERSION}`;
      }
      get versions() {
        return { node: NODE_VERSION };
      }
      get allowedNodeEnvironmentFlags() {
        return /* @__PURE__ */ new Set();
      }
      get sourceMapsEnabled() {
        return false;
      }
      get debugPort() {
        return 0;
      }
      get throwDeprecation() {
        return false;
      }
      get traceDeprecation() {
        return false;
      }
      get features() {
        return {};
      }
      get release() {
        return {};
      }
      get connected() {
        return false;
      }
      get config() {
        return {};
      }
      get moduleLoadList() {
        return [];
      }
      constrainedMemory() {
        return 0;
      }
      availableMemory() {
        return 0;
      }
      uptime() {
        return 0;
      }
      resourceUsage() {
        return {};
      }
      // --- noop methods ---
      ref() {
      }
      unref() {
      }
      // --- unimplemented methods ---
      umask() {
        throw createNotImplementedError("process.umask");
      }
      getBuiltinModule() {
        return void 0;
      }
      getActiveResourcesInfo() {
        throw createNotImplementedError("process.getActiveResourcesInfo");
      }
      exit() {
        throw createNotImplementedError("process.exit");
      }
      reallyExit() {
        throw createNotImplementedError("process.reallyExit");
      }
      kill() {
        throw createNotImplementedError("process.kill");
      }
      abort() {
        throw createNotImplementedError("process.abort");
      }
      dlopen() {
        throw createNotImplementedError("process.dlopen");
      }
      setSourceMapsEnabled() {
        throw createNotImplementedError("process.setSourceMapsEnabled");
      }
      loadEnvFile() {
        throw createNotImplementedError("process.loadEnvFile");
      }
      disconnect() {
        throw createNotImplementedError("process.disconnect");
      }
      cpuUsage() {
        throw createNotImplementedError("process.cpuUsage");
      }
      setUncaughtExceptionCaptureCallback() {
        throw createNotImplementedError("process.setUncaughtExceptionCaptureCallback");
      }
      hasUncaughtExceptionCaptureCallback() {
        throw createNotImplementedError("process.hasUncaughtExceptionCaptureCallback");
      }
      initgroups() {
        throw createNotImplementedError("process.initgroups");
      }
      openStdin() {
        throw createNotImplementedError("process.openStdin");
      }
      assert() {
        throw createNotImplementedError("process.assert");
      }
      binding() {
        throw createNotImplementedError("process.binding");
      }
      // --- attached interfaces ---
      permission = { has: /* @__PURE__ */ notImplemented("process.permission.has") };
      report = {
        directory: "",
        filename: "",
        signal: "SIGUSR2",
        compact: false,
        reportOnFatalError: false,
        reportOnSignal: false,
        reportOnUncaughtException: false,
        getReport: /* @__PURE__ */ notImplemented("process.report.getReport"),
        writeReport: /* @__PURE__ */ notImplemented("process.report.writeReport")
      };
      finalization = {
        register: /* @__PURE__ */ notImplemented("process.finalization.register"),
        unregister: /* @__PURE__ */ notImplemented("process.finalization.unregister"),
        registerBeforeExit: /* @__PURE__ */ notImplemented("process.finalization.registerBeforeExit")
      };
      memoryUsage = Object.assign(() => ({
        arrayBuffers: 0,
        rss: 0,
        external: 0,
        heapTotal: 0,
        heapUsed: 0
      }), { rss: /* @__PURE__ */ __name(() => 0, "rss") });
      // --- undefined props ---
      mainModule = void 0;
      domain = void 0;
      // optional
      send = void 0;
      exitCode = void 0;
      channel = void 0;
      getegid = void 0;
      geteuid = void 0;
      getgid = void 0;
      getgroups = void 0;
      getuid = void 0;
      setegid = void 0;
      seteuid = void 0;
      setgid = void 0;
      setgroups = void 0;
      setuid = void 0;
      // internals
      _events = void 0;
      _eventsCount = void 0;
      _exiting = void 0;
      _maxListeners = void 0;
      _debugEnd = void 0;
      _debugProcess = void 0;
      _fatalException = void 0;
      _getActiveHandles = void 0;
      _getActiveRequests = void 0;
      _kill = void 0;
      _preload_modules = void 0;
      _rawDebug = void 0;
      _startProfilerIdleNotifier = void 0;
      _stopProfilerIdleNotifier = void 0;
      _tickCallback = void 0;
      _disconnect = void 0;
      _handleQueue = void 0;
      _pendingMessage = void 0;
      _channel = void 0;
      _send = void 0;
      _linkedBinding = void 0;
    };
  }
});

// ../../wr/node_modules/@cloudflare/unenv-preset/dist/runtime/node/process.mjs
var globalProcess, getBuiltinModule, workerdProcess, unenvProcess, exit, features, platform, _channel, _debugEnd, _debugProcess, _disconnect, _events, _eventsCount, _exiting, _fatalException, _getActiveHandles, _getActiveRequests, _handleQueue, _kill, _linkedBinding, _maxListeners, _pendingMessage, _preload_modules, _rawDebug, _send, _startProfilerIdleNotifier, _stopProfilerIdleNotifier, _tickCallback, abort, addListener, allowedNodeEnvironmentFlags, arch, argv, argv0, assert2, availableMemory, binding, channel, chdir, config, connected, constrainedMemory, cpuUsage, cwd, debugPort, disconnect, dlopen, domain, emit, emitWarning, env, eventNames, execArgv, execPath, exitCode, finalization, getActiveResourcesInfo, getegid, geteuid, getgid, getgroups, getMaxListeners, getuid, hasUncaughtExceptionCaptureCallback, hrtime3, initgroups, kill, listenerCount, listeners, loadEnvFile, mainModule, memoryUsage, moduleLoadList, nextTick, off, on, once, openStdin, permission, pid, ppid, prependListener, prependOnceListener, rawListeners, reallyExit, ref, release, removeAllListeners, removeListener, report, resourceUsage, send, setegid, seteuid, setgid, setgroups, setMaxListeners, setSourceMapsEnabled, setuid, setUncaughtExceptionCaptureCallback, sourceMapsEnabled, stderr, stdin, stdout, throwDeprecation, title, traceDeprecation, umask, unref, uptime, version, versions, _process, process_default;
var init_process2 = __esm({
  "../../wr/node_modules/@cloudflare/unenv-preset/dist/runtime/node/process.mjs"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    init_hrtime();
    init_process();
    globalProcess = globalThis["process"];
    getBuiltinModule = globalProcess.getBuiltinModule;
    workerdProcess = getBuiltinModule("node:process");
    unenvProcess = new Process({
      env: globalProcess.env,
      hrtime,
      // `nextTick` is available from workerd process v1
      nextTick: workerdProcess.nextTick
    });
    ({ exit, features, platform } = workerdProcess);
    ({
      _channel,
      _debugEnd,
      _debugProcess,
      _disconnect,
      _events,
      _eventsCount,
      _exiting,
      _fatalException,
      _getActiveHandles,
      _getActiveRequests,
      _handleQueue,
      _kill,
      _linkedBinding,
      _maxListeners,
      _pendingMessage,
      _preload_modules,
      _rawDebug,
      _send,
      _startProfilerIdleNotifier,
      _stopProfilerIdleNotifier,
      _tickCallback,
      abort,
      addListener,
      allowedNodeEnvironmentFlags,
      arch,
      argv,
      argv0,
      assert: assert2,
      availableMemory,
      binding,
      channel,
      chdir,
      config,
      connected,
      constrainedMemory,
      cpuUsage,
      cwd,
      debugPort,
      disconnect,
      dlopen,
      domain,
      emit,
      emitWarning,
      env,
      eventNames,
      execArgv,
      execPath,
      exitCode,
      finalization,
      getActiveResourcesInfo,
      getegid,
      geteuid,
      getgid,
      getgroups,
      getMaxListeners,
      getuid,
      hasUncaughtExceptionCaptureCallback,
      hrtime: hrtime3,
      initgroups,
      kill,
      listenerCount,
      listeners,
      loadEnvFile,
      mainModule,
      memoryUsage,
      moduleLoadList,
      nextTick,
      off,
      on,
      once,
      openStdin,
      permission,
      pid,
      ppid,
      prependListener,
      prependOnceListener,
      rawListeners,
      reallyExit,
      ref,
      release,
      removeAllListeners,
      removeListener,
      report,
      resourceUsage,
      send,
      setegid,
      seteuid,
      setgid,
      setgroups,
      setMaxListeners,
      setSourceMapsEnabled,
      setuid,
      setUncaughtExceptionCaptureCallback,
      sourceMapsEnabled,
      stderr,
      stdin,
      stdout,
      throwDeprecation,
      title,
      traceDeprecation,
      umask,
      unref,
      uptime,
      version,
      versions
    } = unenvProcess);
    _process = {
      abort,
      addListener,
      allowedNodeEnvironmentFlags,
      hasUncaughtExceptionCaptureCallback,
      setUncaughtExceptionCaptureCallback,
      loadEnvFile,
      sourceMapsEnabled,
      arch,
      argv,
      argv0,
      chdir,
      config,
      connected,
      constrainedMemory,
      availableMemory,
      cpuUsage,
      cwd,
      debugPort,
      dlopen,
      disconnect,
      emit,
      emitWarning,
      env,
      eventNames,
      execArgv,
      execPath,
      exit,
      finalization,
      features,
      getBuiltinModule,
      getActiveResourcesInfo,
      getMaxListeners,
      hrtime: hrtime3,
      kill,
      listeners,
      listenerCount,
      memoryUsage,
      nextTick,
      on,
      off,
      once,
      pid,
      platform,
      ppid,
      prependListener,
      prependOnceListener,
      rawListeners,
      release,
      removeAllListeners,
      removeListener,
      report,
      resourceUsage,
      setMaxListeners,
      setSourceMapsEnabled,
      stderr,
      stdin,
      stdout,
      title,
      throwDeprecation,
      traceDeprecation,
      umask,
      uptime,
      version,
      versions,
      // @ts-expect-error old API
      domain,
      initgroups,
      moduleLoadList,
      reallyExit,
      openStdin,
      assert: assert2,
      binding,
      send,
      exitCode,
      channel,
      getegid,
      geteuid,
      getgid,
      getgroups,
      getuid,
      setegid,
      seteuid,
      setgid,
      setgroups,
      setuid,
      permission,
      mainModule,
      _events,
      _eventsCount,
      _exiting,
      _maxListeners,
      _debugEnd,
      _debugProcess,
      _fatalException,
      _getActiveHandles,
      _getActiveRequests,
      _kill,
      _preload_modules,
      _rawDebug,
      _startProfilerIdleNotifier,
      _stopProfilerIdleNotifier,
      _tickCallback,
      _disconnect,
      _handleQueue,
      _pendingMessage,
      _channel,
      _send,
      _linkedBinding
    };
    process_default = _process;
  }
});

// ../../wr/node_modules/wrangler/_virtual_unenv_global_polyfill-@cloudflare-unenv-preset-node-process
var init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process = __esm({
  "../../wr/node_modules/wrangler/_virtual_unenv_global_polyfill-@cloudflare-unenv-preset-node-process"() {
    init_process2();
    globalThis.process = process_default;
  }
});

// ../lib/company-core.mjs
async function bget(key) {
  if (!STORE) return memo.get(key) || null;
  try {
    return await STORE.getJSON(key);
  } catch (e) {
    return null;
  }
}
async function bset(key, val) {
  if (!STORE) {
    memo.set(key, val);
    return;
  }
  try {
    await STORE.setJSON(key, val);
  } catch (e) {
  }
}
function normalizeUrl(raw) {
  let s = String(raw || "").trim();
  if (!s || s.length > 300) return null;
  if (!/^https?:\/\//i.test(s)) s = "https://" + s;
  let u;
  try {
    u = new URL(s);
  } catch (e) {
    return null;
  }
  if (!/^https?:$/.test(u.protocol)) return null;
  const host = u.hostname.toLowerCase();
  if (!host.includes(".") || host.endsWith(".local") || host === "localhost" || /^\d+\.\d+\.\d+\.\d+$/.test(host) || host.includes(":")) return null;
  return { home: "https://" + host + "/", host: host.replace(/^www\./, "") };
}
function prompt(home, host) {
  return [
    `Research the company whose homepage is ${home} (domain ${host}). Build a market snapshot for a go to market strategist.`,
    "Start on the homepage, then the about, customers, pricing and press pages, then search the web: Crunchbase, LinkedIn, company filings and investor relations, reputable press, G2 or Gartner Peer Insights reviews, job postings.",
    "Find: market cap (or latest private valuation), headquarters, employee count, total customers, ARR (or annual revenue), top 5 competitors, unique differentiators, why customers choose them over competitors, growth pain points, and revenue opportunities they are missing with the fix for each.",
    'Rules. Never invent a number. If a figure is not published, set value to "Not disclosed" and confidence to UNVERIFIED. Prefer the most recent figure and set as_of. Put the source URL on every figure.',
    "Keep every text field short and specific, the way an analyst writes a one pager. No marketing language, no em dashes, no semicolons.",
    "Pain points and missed revenue are your analysis: base each on a visible signal (pricing page gaps, missing segments, regions not served, review complaints, hiring patterns, no partner program, no marketplace listings, weak self serve, no expansion pricing) and say what the signal is.",
    "List the pages you relied on in sources."
  ].join("\n");
}
function tidyFact(f) {
  f = f && typeof f === "object" ? f : { value: typeof f === "string" ? f : "" };
  const value = clip(f.value, 70) || "Not disclosed";
  const conf = ["HIGH", "MEDIUM", "UNVERIFIED"].includes(String(f.confidence).toUpperCase()) ? String(f.confidence).toUpperCase() : "UNVERIFIED";
  return { value, as_of: clip(f.as_of, 20), confidence: /not disclosed/i.test(value) ? "UNVERIFIED" : conf, source_url: okUrl(f.source_url) };
}
function tidy(d, host) {
  d = d && typeof d === "object" ? d : {};
  return {
    domain: host,
    company_name: clip(d.company_name, 60) || host,
    one_liner: clip(d.one_liner, 160),
    category: clip(d.category, 50),
    founded: clip(d.founded, 10),
    ownership: clip(d.ownership, 14),
    ticker: clip(d.ticker, 24),
    market_cap: tidyFact(d.market_cap),
    headquarters: tidyFact(d.headquarters),
    employee_count: tidyFact(d.employee_count),
    total_customers: tidyFact(d.total_customers),
    arr: tidyFact(d.arr),
    competitors: arr(d.competitors, 5).map((c) => ({ name: clip(c.name, 40), overlap: clip(c.overlap, 110) })).filter((c) => c.name),
    differentiators: arr(d.differentiators, 5).map((x) => clip(typeof x === "string" ? x : x && x.text, 130)).filter(Boolean),
    why_customers_choose: arr(d.why_customers_choose, 4).map((c) => ({ reason: clip(c.reason, 100), evidence: clip(c.evidence, 150) })).filter((c) => c.reason),
    growth_painpoints: arr(d.growth_painpoints, 6).map((p) => ({ pain: clip(p.pain, 120), severity: p.severity === "nice_to_fix" ? "nice_to_fix" : "must_fix", signal: clip(p.signal, 120) })).filter((p) => p.pain),
    missed_revenue: arr(d.missed_revenue, 5).map((m) => ({ opportunity: clip(m.opportunity, 100), fix: clip(m.fix, 140), impact: ["High", "Medium", "Low"].includes(m.impact) ? m.impact : "Medium" })).filter((m) => m.opportunity),
    sources: arr(d.sources, 10).map((s) => ({ title: clip(s.title, 80), url: okUrl(s.url) })).filter((s) => s.url),
    researched_at: (/* @__PURE__ */ new Date()).toISOString()
  };
}
async function fc(path, opts = {}) {
  const key = process.env.FIRECRAWL_API_KEY;
  const res = await fetch(API + path, { ...opts, headers: { Authorization: "Bearer " + key, "Content-Type": "application/json", ...opts.headers || {} } });
  let body = null;
  try {
    body = await res.json();
  } catch (e) {
  }
  if (!res.ok || body && body.success === false) {
    const msg = body && (body.error || body.message) || "Firecrawl returned " + res.status;
    const err = new Error(String(msg).slice(0, 200));
    err.status = res.status;
    throw err;
  }
  return body || {};
}
function rateLimited(ip) {
  const lim = Number(process.env.COMPANY_RESEARCH_PER_IP_HOUR || 3);
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < 3600 * 1e3);
  if (list.length >= lim) {
    hits.set(ip, list);
    return true;
  }
  list.push(now);
  hits.set(ip, list);
  return false;
}
async function start(req, context2) {
  let body = {};
  try {
    body = await req.json();
  } catch (e) {
  }
  const t = normalizeUrl(body.url);
  if (!t) return json(400, { ok: false, error: "Enter a company homepage, for example accuknox.com." });
  const fresh = !!body.refresh;
  const cached = await bget("r/" + t.host);
  if (cached && !fresh && Date.now() - Date.parse(cached.researched_at) < CACHE_DAYS * 864e5) return json(200, { ok: true, status: "completed", cached: true, data: cached });
  if (process.env.COMPANY_RESEARCH_MOCK === "1") return json(200, { ok: true, status: "completed", mock: true, data: tidy({ ...MOCK }, t.host) });
  if (!process.env.FIRECRAWL_API_KEY) return json(503, { ok: false, error: "Live research is switching on shortly. Book a call and I will run this company for you in the meantime." });
  const ip = context2 && context2.ip || req.headers.get("x-nf-client-connection-ip") || "anon";
  if (rateLimited(ip)) return json(429, { ok: false, error: "You have run 3 new reports this hour. Cached companies still load instantly, new ones open up again within the hour." });
  const day = (/* @__PURE__ */ new Date()).toISOString().slice(0, 10);
  const cap = Number(process.env.COMPANY_RESEARCH_DAILY_CAP || 25);
  const used = await bget("d/" + day) || { n: 0 };
  if (used.n >= cap) return json(429, { ok: false, error: "Today's research quota is used up. Try again tomorrow, or book a call and I will run it for you." });
  const payload = { prompt: prompt(t.home, t.host), urls: [t.home], schema: SCHEMA, maxCredits: Number(process.env.COMPANY_RESEARCH_MAX_CREDITS || 400) };
  if (process.env.FIRECRAWL_AGENT_MODEL) payload.model = process.env.FIRECRAWL_AGENT_MODEL;
  try {
    const r = await fc("/agent", { method: "POST", body: JSON.stringify(payload) });
    if (!r.id) throw new Error("Firecrawl did not return a job id.");
    await bset("j/" + r.id, { host: t.host, at: Date.now() });
    await bset("d/" + day, { n: used.n + 1 });
    return json(202, { ok: true, status: "processing", id: r.id, host: t.host });
  } catch (e) {
    return json(502, { ok: false, error: e.status === 402 ? "The Firecrawl account is out of credits." : "Could not start the research: " + e.message });
  }
}
async function poll(id, hostHint) {
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id)) return json(400, { ok: false, error: "Bad job id." });
  if (!process.env.FIRECRAWL_API_KEY) return json(503, { ok: false, error: "Company research is not connected yet." });
  const job = await bget("j/" + id);
  try {
    const r = await fc("/agent/" + id, { method: "GET" });
    if (r.status === "processing") return json(200, { ok: true, status: "processing" });
    if (r.status !== "completed") return json(200, { ok: false, status: r.status, error: r.error ? "Research failed: " + String(r.error).slice(0, 160) : "Research was " + r.status + ". Try again." });
    let data = r.data;
    if (typeof data === "string") {
      try {
        data = JSON.parse(data);
      } catch (e) {
      }
    }
    const hint = normalizeUrl(hostHint);
    const host = job && job.host || hint && hint.host || "company";
    const clean = tidy(data, host);
    clean.credits_used = r.creditsUsed ?? null;
    if (job) await bset("r/" + host, clean);
    return json(200, { ok: true, status: "completed", data: clean });
  } catch (e) {
    return json(502, { ok: false, error: "Could not read the research job: " + e.message });
  }
}
async function handle(req, context2, storeImpl) {
  STORE = storeImpl || null;
  if (req.method === "POST") return start(req, context2);
  if (req.method === "GET") {
    const q = new URL(req.url).searchParams;
    return poll(q.get("id") || "", q.get("host") || "");
  }
  return json(405, { ok: false, error: "Use POST or GET." });
}
var API, CACHE_DAYS, hits, json, STORE, memo, fact, SCHEMA, clip, okUrl, arr, MOCK;
var init_company_core = __esm({
  "../lib/company-core.mjs"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    API = "https://api.firecrawl.dev/v2";
    CACHE_DAYS = 7;
    hits = /* @__PURE__ */ new Map();
    json = /* @__PURE__ */ __name((status, body) => new Response(JSON.stringify(body), {
      status,
      headers: { "Content-Type": "application/json", "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" }
    }), "json");
    STORE = null;
    memo = /* @__PURE__ */ new Map();
    __name(bget, "bget");
    __name(bset, "bset");
    __name(normalizeUrl, "normalizeUrl");
    fact = /* @__PURE__ */ __name((desc) => ({
      type: "object",
      properties: {
        value: { type: "string", description: desc },
        as_of: { type: "string", description: 'Month and year the figure refers to, for example "Mar 2026". Empty if unknown.' },
        confidence: { type: "string", enum: ["HIGH", "MEDIUM", "UNVERIFIED"], description: "HIGH = company filing or official page. MEDIUM = reputable press or analyst estimate. UNVERIFIED = single weak source or inference." },
        source_url: { type: "string", description: "URL of the page the figure came from. Empty if none." }
      },
      required: ["value", "confidence"]
    }), "fact");
    SCHEMA = {
      type: "object",
      properties: {
        company_name: { type: "string" },
        one_liner: { type: "string", description: "What the company sells and to whom, max 18 words." },
        category: { type: "string", description: 'Market category in 2 to 4 words, for example "Cloud security (CNAPP)".' },
        founded: { type: "string", description: "Year founded, or empty." },
        ownership: { type: "string", enum: ["Public", "Private", "Subsidiary", "Unknown"] },
        ticker: { type: "string", description: 'Exchange and ticker if public, for example "NASDAQ: CRWD". Empty otherwise.' },
        market_cap: fact('Public: market capitalisation in USD, for example "$84.2B". Private: latest post money valuation with the word "valuation", for example "$1.2B valuation (Series D)". If neither is disclosed: "Not disclosed".'),
        headquarters: fact('City, region and country of the head office, for example "Austin, Texas, USA".'),
        employee_count: fact('Headcount as a number or range, for example "1,250" or "500 to 1,000".'),
        total_customers: fact('Number of customers, for example "3,500+ customers". "Not disclosed" if the company never states it.'),
        arr: fact('Annual recurring revenue in USD, for example "$120M ARR". Public companies without ARR: latest annual revenue labelled "revenue". "Not disclosed" if unknown.'),
        competitors: {
          type: "array",
          maxItems: 5,
          items: { type: "object", properties: {
            name: { type: "string" },
            overlap: { type: "string", description: "Where they compete head to head, max 12 words." }
          }, required: ["name", "overlap"] }
        },
        differentiators: { type: "array", maxItems: 5, items: { type: "string", description: "One unique differentiator, max 16 words, concrete and specific." } },
        why_customers_choose: {
          type: "array",
          maxItems: 4,
          items: { type: "object", properties: {
            reason: { type: "string", description: "Why buyers pick them over competitors, max 12 words." },
            evidence: { type: "string", description: "Proof: a review theme, case study result, customer quote paraphrase or award, max 18 words." }
          }, required: ["reason", "evidence"] }
        },
        growth_painpoints: {
          type: "array",
          maxItems: 6,
          items: { type: "object", properties: {
            pain: { type: "string", description: "A growth pain point of this company, max 14 words." },
            severity: { type: "string", enum: ["must_fix", "nice_to_fix"], description: "must_fix = actively limiting growth now. nice_to_fix = drag on efficiency." },
            signal: { type: "string", description: "What points to it: reviews, hiring, pricing page, press, churn talk. Max 14 words." }
          }, required: ["pain", "severity"] }
        },
        missed_revenue: {
          type: "array",
          maxItems: 5,
          items: { type: "object", properties: {
            opportunity: { type: "string", description: "A revenue opportunity the company is under using, max 12 words." },
            fix: { type: "string", description: "The concrete fix, max 16 words." },
            impact: { type: "string", enum: ["High", "Medium", "Low"] }
          }, required: ["opportunity", "fix", "impact"] }
        },
        sources: {
          type: "array",
          maxItems: 10,
          items: { type: "object", properties: { title: { type: "string" }, url: { type: "string" } }, required: ["url"] }
        }
      },
      required: ["company_name", "one_liner", "market_cap", "headquarters", "employee_count", "total_customers", "arr", "competitors", "differentiators", "why_customers_choose", "growth_painpoints", "missed_revenue"]
    };
    __name(prompt, "prompt");
    clip = /* @__PURE__ */ __name((s, n) => {
      s = String(s == null ? "" : s).replace(/\s*[—–]\s*/g, ", ").replace(/;\s*/g, ", ").replace(/\s+/g, " ").trim();
      return s.length > n ? s.slice(0, n - 1).replace(/\s+\S*$/, "") + "\u2026" : s;
    }, "clip");
    okUrl = /* @__PURE__ */ __name((u) => {
      try {
        const x = new URL(String(u));
        return /^https?:$/.test(x.protocol) ? x.href : "";
      } catch (e) {
        return "";
      }
    }, "okUrl");
    __name(tidyFact, "tidyFact");
    arr = /* @__PURE__ */ __name((a, n) => (Array.isArray(a) ? a : []).filter(Boolean).slice(0, n), "arr");
    __name(tidy, "tidy");
    MOCK = {
      company_name: "Example Security",
      one_liner: "Cloud security platform for mid market engineering teams running Kubernetes.",
      category: "Cloud security (CNAPP)",
      founded: "2019",
      ownership: "Private",
      ticker: "",
      market_cap: { value: "$450M valuation (Series C)", as_of: "Jun 2025", confidence: "MEDIUM", source_url: "https://example.com/press" },
      headquarters: { value: "San Jose, California, USA", confidence: "HIGH", source_url: "https://example.com/about" },
      employee_count: { value: "320", as_of: "Oct 2026", confidence: "MEDIUM", source_url: "https://www.linkedin.com/company/example" },
      total_customers: { value: "600+ customers", confidence: "HIGH", source_url: "https://example.com/customers" },
      arr: { value: "Not disclosed", confidence: "UNVERIFIED" },
      competitors: [{ name: "Wiz", overlap: "Agentless CSPM and cloud risk graph" }, { name: "Palo Alto Prisma Cloud", overlap: "Enterprise CNAPP suites" }, { name: "Sysdig", overlap: "Runtime detection for containers" }, { name: "Aqua Security", overlap: "Container image and runtime security" }],
      differentiators: ["Runtime enforcement in the kernel, not only detection", "Deploys on prem and air gapped for regulated buyers", "Open source core with an active community"],
      why_customers_choose: [{ reason: "Blocks attacks at runtime instead of alerting", evidence: "G2 reviews cite fewer incidents after rollout" }, { reason: "Lower total cost than suites", evidence: "Case study reports 40% lower spend than prior stack" }],
      growth_painpoints: [{ pain: "Brand awareness trails better funded rivals", severity: "must_fix", signal: "Low share of voice in analyst reports" }, { pain: "Long enterprise sales cycles", severity: "must_fix", signal: "Hiring for enterprise AEs in 4 regions" }, { pain: "No self serve trial", severity: "nice_to_fix", signal: "Pricing page routes every visitor to sales" }],
      missed_revenue: [{ opportunity: "Cloud marketplace private offers", fix: "List on AWS, Azure and GCP marketplaces with committed spend drawdown", impact: "High" }, { opportunity: "MSSP channel", fix: "Launch a partner program with multi tenant pricing", impact: "High" }, { opportunity: "Expansion revenue", fix: "Price per workload with clear tiers to drive upsell", impact: "Medium" }],
      sources: [{ title: "Example homepage", url: "https://example.com/" }]
    };
    __name(fc, "fc");
    __name(rateLimited, "rateLimited");
    __name(start, "start");
    __name(poll, "poll");
    __name(handle, "handle");
  }
});

// ../lib/platform.js
function loadEnv(env2) {
  if (typeof process === "undefined") globalThis.process = { env: {} };
  process.env = process.env || {};
  for (const [k, v] of Object.entries(env2 || {})) if (typeof v === "string") process.env[k] = v;
}
function clientIp(request) {
  return request.headers.get("cf-connecting-ip") || request.headers.get("x-forwarded-for") || "anon";
}
function v1(handler) {
  return async (context2) => {
    loadEnv(context2.env);
    const req = context2.request;
    const url = new URL(req.url);
    const headers = Object.fromEntries(req.headers.entries());
    headers["x-nf-client-connection-ip"] = clientIp(req);
    const event = {
      httpMethod: req.method,
      path: url.pathname,
      headers,
      queryStringParameters: Object.fromEntries(url.searchParams.entries()),
      body: req.method === "GET" || req.method === "HEAD" ? null : await req.text(),
      isBase64Encoded: false
    };
    try {
      const r = await handler(event, {}) || {};
      return new Response(r.body ?? "", { status: r.statusCode || 200, headers: r.headers || {} });
    } catch (e) {
      return new Response(JSON.stringify({ ok: false, error: "Server error." }), { status: 500, headers: { "Content-Type": "application/json" } });
    }
  };
}
function kvStore(kv, ttlDays) {
  if (!kv) return null;
  return {
    getJSON: /* @__PURE__ */ __name((k) => kv.get(k, "json"), "getJSON"),
    setJSON: /* @__PURE__ */ __name((k, v) => kv.put(k, JSON.stringify(v), ttlDays ? { expirationTtl: Math.round(ttlDays * 86400) } : void 0), "setJSON")
  };
}
var init_platform = __esm({
  "../lib/platform.js"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    __name(loadEnv, "loadEnv");
    __name(clientIp, "clientIp");
    __name(v1, "v1");
    __name(kvStore, "kvStore");
  }
});

// api/company-research.js
async function onRequest(context2) {
  loadEnv(context2.env);
  return handle(context2.request, { ip: clientIp(context2.request) }, kvStore(context2.env.CR_KV, 8));
}
var init_company_research = __esm({
  "api/company-research.js"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    init_company_core();
    init_platform();
    __name(onRequest, "onRequest");
  }
});

// ../netlify/functions/salary-report.js
var require_salary_report = __commonJS({
  "../netlify/functions/salary-report.js"(exports) {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    var MAX_PDF_BYTES = 4 * 1024 * 1024;
    var EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
    var hits2 = /* @__PURE__ */ new Map();
    function json2(status, body) {
      return {
        statusCode: status,
        headers: { "Content-Type": "application/json", "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" },
        body: JSON.stringify(body)
      };
    }
    __name(json2, "json");
    function esc(s) {
      return String(s || "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
    }
    __name(esc, "esc");
    exports.handler = async function(event) {
      if (event.httpMethod !== "POST") return json2(405, { ok: false, error: "Use POST." });
      const key = process.env.BREVO_API_KEY;
      if (!key) return json2(503, { ok: false, error: "Email is not set up yet on this site." });
      const ip = (event.headers["x-nf-client-connection-ip"] || event.headers["client-ip"] || "unknown").split(",")[0].trim();
      const now = Date.now();
      const rec = hits2.get(ip) || [];
      const recent = rec.filter((t) => now - t < 10 * 60 * 1e3);
      if (recent.length >= 5) return json2(429, { ok: false, error: "Too many reports from this connection. Try again in a few minutes." });
      recent.push(now);
      hits2.set(ip, recent);
      let data;
      try {
        data = JSON.parse(event.body || "{}");
      } catch (e) {
        return json2(400, { ok: false, error: "Bad request body." });
      }
      const email = String(data.email || "").trim().toLowerCase();
      const name = String(data.name || "").trim().slice(0, 60);
      const pdf = String(data.pdf || "");
      const filename = /^[a-z0-9-]+\.pdf$/i.test(String(data.filename || "")) ? data.filename : "salary-growth-report.pdf";
      const s = data.summary || {};
      if (!EMAIL_RE.test(email)) return json2(400, { ok: false, error: "Enter a valid email address." });
      if (!pdf || pdf.length > MAX_PDF_BYTES || !/^[A-Za-z0-9+/=]+$/.test(pdf)) return json2(400, { ok: false, error: "The PDF payload is missing or too large." });
      const senderEmail = process.env.REPORT_SENDER_EMAIL || "ssyedhadi14@gmail.com";
      const senderName = process.env.REPORT_SENDER_NAME || "Syed Hadi";
      const replyTo = process.env.REPORT_REPLY_TO || "ssyedhadi14@gmail.com";
      const bcc = (process.env.REPORT_BCC || "").split(",").map((x) => x.trim()).filter((x) => EMAIL_RE.test(x));
      const first = name ? esc(name.split(" ")[0]) : "there";
      const link = /^https:\/\/syedcreates\.com\//.test(String(s.link || "")) ? String(s.link) : "https://syedcreates.com/salary-calculator";
      const html = `<!doctype html><html><body style="margin:0;background:#f6f5fb;font-family:Verdana,Geneva,sans-serif;color:#141228">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:28px 12px">
<table role="presentation" width="100%" style="max-width:560px;background:#ffffff;border-radius:16px;overflow:hidden">
<tr><td style="background:#5b3df5;padding:26px 28px;color:#fff;font-size:20px;font-weight:bold;font-family:Verdana,Geneva,sans-serif">Your salary growth report</td></tr>
<tr><td style="padding:26px 28px;font-size:14px;line-height:1.6;font-family:Verdana,Geneva,sans-serif">
<p style="margin:0 0 14px">Hi ${first},</p>
<p style="margin:0 0 14px">The PDF is attached. Here is the short version:</p>
<table role="presentation" cellpadding="0" cellspacing="0" style="font-size:14px;font-family:Verdana,Geneva,sans-serif;margin:0 0 16px">
<tr><td style="padding:6px 14px 6px 0;color:#6b6b82">Corpus at age ${esc(s.target)}</td><td style="padding:6px 0;font-weight:bold">${esc(s.corpus)}</td></tr>
<tr><td style="padding:6px 14px 6px 0;color:#6b6b82">In today&rsquo;s money</td><td style="padding:6px 0;font-weight:bold">${esc(s.real)}</td></tr>
<tr><td style="padding:6px 14px 6px 0;color:#6b6b82">You invest per month now</td><td style="padding:6px 0;font-weight:bold">${esc(s.investNow)}</td></tr>
</table>
<p style="margin:0 0 18px"><a href="${esc(link)}" style="display:inline-block;background:#5b3df5;color:#fff;text-decoration:none;padding:12px 18px;border-radius:10px;font-weight:bold">Reopen your plan</a></p>
<p style="margin:0 0 14px">Two things that change the curve most: the increment you negotiate and the share of salary you invest. If you want to talk through either, reply to this email or <a href="https://syedcreates.com/schedule-meeting" style="color:#5b3df5">book 30 minutes</a>.</p>
<p style="margin:0;color:#6b6b82;font-size:12px">Planning tool, not investment advice. Returns are assumptions, not predictions. You asked for this one email from syedcreates.com. There is no list to unsubscribe from.</p>
</td></tr>
<tr><td style="padding:16px 28px;background:#f6f5fb;font-size:12px;color:#6b6b82;font-family:Verdana,Geneva,sans-serif">Syed Hadi &middot; Product Marketing and Partnerships Lead &middot; Bengaluru &middot; <a href="https://syedcreates.com" style="color:#5b3df5">syedcreates.com</a></td></tr>
</table></td></tr></table></body></html>`;
      const payload = {
        sender: { name: senderName, email: senderEmail },
        to: [{ email, name: name || void 0 }],
        replyTo: { email: replyTo, name: senderName },
        subject: `Your salary growth report: ${String(s.corpus || "").replace(/[^\w\s.₹]/g, "")} at age ${String(s.target || "").replace(/\D/g, "")}`.trim(),
        htmlContent: html,
        textContent: `Hi ${first},

Your salary growth report is attached.
Corpus at age ${s.target}: ${s.corpus} (${s.real} in today's money). You invest ${s.investNow} per month now.
Reopen your plan: ${link}

Planning tool, not investment advice.
Syed Hadi, syedcreates.com`,
        attachment: [{ content: pdf, name: filename }],
        tags: ["salary-calculator"]
      };
      if (bcc.length) payload.bcc = bcc.map((e) => ({ email: e }));
      try {
        const res = await fetch("https://api.brevo.com/v3/smtp/email", {
          method: "POST",
          headers: { "api-key": key, "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(payload)
        });
        if (!res.ok) {
          const txt = await res.text();
          console.error("brevo error", res.status, txt.slice(0, 300));
          return json2(502, { ok: false, error: "The mail service rejected the message." });
        }
        return json2(200, { ok: true });
      } catch (err) {
        console.error("send failed", err && err.message);
        return json2(502, { ok: false, error: "Could not reach the mail service." });
      }
    };
  }
});

// api/salary-report.js
var import_salary_report, onRequest2;
var init_salary_report = __esm({
  "api/salary-report.js"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    import_salary_report = __toESM(require_salary_report());
    init_platform();
    onRequest2 = v1(import_salary_report.default.handler);
  }
});

// ../netlify/functions/seo-aeo-score.js
var require_seo_aeo_score = __commonJS({
  "../netlify/functions/seo-aeo-score.js"(exports) {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    var UA = "Mozilla/5.0 (compatible; SyedCreatesScoreBot/1.0; +https://syedcreates.com/seo-aeo-score)";
    var MAX_HTML = 1.5 * 1024 * 1024;
    var hits2 = /* @__PURE__ */ new Map();
    var drCache = /* @__PURE__ */ new Map();
    var projectIdCache = null;
    function json2(status, body) {
      return { statusCode: status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" }, body: JSON.stringify(body) };
    }
    __name(json2, "json");
    function normalizeUrl2(raw) {
      let s = String(raw || "").trim();
      if (!s) return null;
      if (!/^https?:\/\//i.test(s)) s = "https://" + s;
      let u;
      try {
        u = new URL(s);
      } catch (e) {
        return null;
      }
      if (!/^https?:$/.test(u.protocol)) return null;
      const host = u.hostname.toLowerCase();
      if (process.env.ALLOW_LOCAL_TARGETS === "1" && (host === "localhost" || host === "127.0.0.1")) return u;
      if (!host.includes(".") || host.endsWith(".local") || host === "localhost" || /^\d+\.\d+\.\d+\.\d+$/.test(host) || host.includes(":")) return null;
      if (/^(10\.|127\.|169\.254\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)/.test(host)) return null;
      u.hash = "";
      return u;
    }
    __name(normalizeUrl2, "normalizeUrl");
    async function fetchText(url, { timeout = 1e4, max = MAX_HTML, accept = "text/html,application/xhtml+xml,*/*;q=0.8" } = {}) {
      const ctl = new AbortController();
      const t = setTimeout(() => ctl.abort(), timeout);
      const started = Date.now();
      try {
        const res = await fetch(url, { redirect: "follow", signal: ctl.signal, headers: { "User-Agent": UA, Accept: accept, "Accept-Language": "en" } });
        const reader = res.body && res.body.getReader ? res.body.getReader() : null;
        let text = "";
        if (reader) {
          const dec = new TextDecoder();
          let got = 0;
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            got += value.length;
            text += dec.decode(value, { stream: true });
            if (got > max) {
              try {
                ctl.abort();
              } catch (e) {
              }
              break;
            }
          }
        } else {
          text = await res.text();
        }
        return { ok: res.ok, status: res.status, url: res.url, text, ms: Date.now() - started, headers: Object.fromEntries(res.headers.entries()), redirected: res.redirected };
      } catch (e) {
        return { ok: false, status: 0, url, text: "", ms: Date.now() - started, headers: {}, error: e.name === "AbortError" ? "timeout" : e.message };
      } finally {
        clearTimeout(t);
      }
    }
    __name(fetchText, "fetchText");
    function strip(html) {
      return html.replace(/<script[\s\S]*?<\/script>/gi, " ").replace(/<style[\s\S]*?<\/style>/gi, " ");
    }
    __name(strip, "strip");
    function textOf(html) {
      return strip(html).replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/&amp;/g, "&").replace(/\s+/g, " ").trim();
    }
    __name(textOf, "textOf");
    function tag(html, re) {
      const m = html.match(re);
      return m ? m[1].trim() : "";
    }
    __name(tag, "tag");
    function metaContent(html, nameOrProp) {
      const re1 = new RegExp(`<meta[^>]+(?:name|property)=["']` + nameOrProp + `["'][^>]*content=["']([^"']*)["']`, "i");
      const re2 = new RegExp(`<meta[^>]+content=["']([^"']*)["'][^>]*(?:name|property)=["']` + nameOrProp + `["']`, "i");
      return tag(html, re1) || tag(html, re2);
    }
    __name(metaContent, "metaContent");
    function headings(html) {
      const out = [];
      const re = /<h([1-6])\b[^>]*>([\s\S]*?)<\/h\1>/gi;
      let m;
      while (m = re.exec(strip(html))) out.push({ level: +m[1], text: textOf(m[2]) });
      return out;
    }
    __name(headings, "headings");
    function jsonLd(html) {
      const out = [];
      const re = /<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi;
      let m;
      while (m = re.exec(html)) {
        try {
          out.push(JSON.parse(m[1].trim()));
        } catch (e) {
          out.push({ __invalid: true });
        }
      }
      return out;
    }
    __name(jsonLd, "jsonLd");
    function ldTypes(blocks) {
      const types = /* @__PURE__ */ new Set();
      const walk = /* @__PURE__ */ __name((n) => {
        if (!n || typeof n !== "object") return;
        if (Array.isArray(n)) return n.forEach(walk);
        if (n["@type"]) [].concat(n["@type"]).forEach((t) => types.add(String(t)));
        if (n["@graph"]) walk(n["@graph"]);
        Object.keys(n).forEach((k) => {
          if (k !== "@graph" && typeof n[k] === "object") walk(n[k]);
        });
      }, "walk");
      blocks.forEach(walk);
      return types;
    }
    __name(ldTypes, "ldTypes");
    function wordCount(s) {
      return s ? s.split(/\s+/).filter(Boolean).length : 0;
    }
    __name(wordCount, "wordCount");
    async function openseoCall(name, args, key) {
      const res = await fetch("https://app.openseo.so/mcp", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json, text/event-stream", Authorization: "Bearer " + key },
        body: JSON.stringify({ jsonrpc: "2.0", id: Date.now(), method: "tools/call", params: { name, arguments: args } })
      });
      const ct = res.headers.get("content-type") || "";
      const raw = await res.text();
      let msg = null;
      if (ct.includes("text/event-stream")) {
        raw.split("\n").forEach((line) => {
          if (line.startsWith("data:")) {
            try {
              const j = JSON.parse(line.slice(5).trim());
              if (j && j.result) msg = j;
            } catch (e) {
            }
          }
        });
      } else {
        try {
          msg = JSON.parse(raw);
        } catch (e) {
        }
      }
      if (!res.ok || !msg || msg.error) throw new Error(msg && msg.error && msg.error.message || "OpenSEO " + res.status);
      return msg.result;
    }
    __name(openseoCall, "openseoCall");
    async function domainRating(host) {
      const key = process.env.OPENSEO_API_KEY;
      if (!key) return { connected: false, note: "OpenSEO is not connected on this site yet." };
      const cached = drCache.get(host);
      if (cached && Date.now() - cached.at < 12 * 3600 * 1e3) return cached.val;
      try {
        let projectId = process.env.OPENSEO_PROJECT_ID || projectIdCache;
        if (!projectId) {
          const lp = await openseoCall("list_projects", {}, key);
          const projects = lp.structuredContent && lp.structuredContent.projects || [];
          if (!projects.length) throw new Error("No OpenSEO project found. Create one in the OpenSEO app.");
          projectId = projects[0].id;
          projectIdCache = projectId;
        }
        const r = await openseoCall("get_backlinks_overview", { projectId, target: host, scope: "domain", hideSpam: true }, key);
        const sc = r.structuredContent || {};
        const summary = sc.overview && sc.overview.overview && sc.overview.overview.summary || sc.overview && sc.overview.summary || {};
        const rank = Number(summary.rank);
        const val = {
          connected: true,
          rank: isFinite(rank) ? rank : null,
          rating: isFinite(rank) ? Math.max(0, Math.min(100, Math.round(rank / 10))) : null,
          backlinks: summary.backlinks ?? null,
          referringDomains: summary.referringDomains ?? null,
          referringPages: summary.referringPages ?? null,
          spamScore: summary.targetSpamScore ?? summary.backlinksSpamScore ?? null,
          newReferringDomains: summary.newReferringDomains ?? null,
          lostReferringDomains: summary.lostReferringDomains ?? null,
          source: "OpenSEO (DataForSEO backlinks), domain scope"
        };
        drCache.set(host, { at: Date.now(), val });
        return val;
      } catch (e) {
        return { connected: true, error: String(e.message || e).slice(0, 160) };
      }
    }
    __name(domainRating, "domainRating");
    function score(page, robots, sitemap, llms, u) {
      const html = page.text || "";
      const checks = [];
      const add = /* @__PURE__ */ __name((group3, id, label, pass, max, detail, action, priority) => checks.push({ group: group3, id, label, pass: !!pass, points: pass ? max : 0, max, detail, action: pass ? "" : action, priority: priority || (max >= 6 ? "high" : max >= 4 ? "medium" : "low") }), "add");
      const title2 = textOf(tag(html, /<title[^>]*>([\s\S]*?)<\/title>/i));
      const desc = metaContent(html, "description");
      const canon = tag(html, /<link[^>]+rel=["']canonical["'][^>]*href=["']([^"']+)["']/i) || tag(html, /<link[^>]+href=["']([^"']+)["'][^>]*rel=["']canonical["']/i);
      const hs = headings(html);
      const h1s = hs.filter((h) => h.level === 1);
      const imgs = strip(html).match(/<img\b[^>]*>/gi) || [];
      const imgsNoAlt = imgs.filter((t) => !/\salt=/i.test(t)).length;
      const links = strip(html).match(/<a\b[^>]*href=["']([^"'#][^"']*)["']/gi) || [];
      const host = u.hostname.replace(/^www\./, "");
      const internal = links.filter((a) => {
        const m = a.match(/href=["']([^"']+)["']/i);
        if (!m) return false;
        const h = m[1];
        return h.startsWith("/") || h.includes(host);
      }).length;
      const ld = jsonLd(html);
      const types = ldTypes(ld);
      const invalidLd = ld.some((b) => b.__invalid);
      const body = textOf(html);
      const words = wordCount(body);
      const viewport = /<meta[^>]+name=["']viewport["']/i.test(html);
      const lang = /<html[^>]+lang=["'][a-z]/i.test(html);
      const og = ["og:title", "og:description", "og:image"].filter((p) => metaContent(html, p)).length;
      const robotsMeta = (metaContent(html, "robots") || "").toLowerCase();
      const robotsTxt = robots.ok ? robots.text : "";
      const blocksAll = /user-agent:\s*\*\s*[\r\n]+(?:[^\n]*\n)*?\s*disallow:\s*\/\s*$/im.test(robotsTxt);
      const aiBots = ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "OAI-SearchBot"];
      const blockedBots = aiBots.filter((b) => new RegExp("user-agent:\\s*" + b + "\\s*[\\r\\n]+(?:[^\\n]*\\n)*?\\s*disallow:\\s*/\\s*$", "im").test(robotsTxt));
      const qHeads = hs.filter((h) => h.level >= 2 && /\?\s*$/.test(h.text)).length;
      const firstPara = (() => {
        const m = strip(html).match(/<h1\b[^>]*>[\s\S]*?<\/h1>[\s\S]*?<p\b[^>]*>([\s\S]*?)<\/p>/i);
        return m ? wordCount(textOf(m[1])) : 0;
      })();
      const hasDates = /<time\b|datePublished|dateModified|article:published_time/i.test(html);
      const hasAuthor = /rel=["']author["']|"author"\s*:|name=["']author["']/i.test(html);
      let jumps = 0;
      let prev = 0;
      hs.forEach((h) => {
        if (prev && h.level > prev + 1) jumps++;
        prev = h.level;
      });
      const sizeKb = Math.round(Buffer.byteLength(html, "utf8") / 1024);
      const inlineScripts = (html.match(/<script\b(?![^>]*src=)[^>]*>/gi) || []).length;
      add("seo", "https", "Served over HTTPS", u.protocol === "https:" && (page.url || "").startsWith("https://"), 5, page.url, "Move the site to HTTPS and redirect every http URL with a 301.");
      add("seo", "status", "Page loads with status 200 in under 3 seconds", page.ok && page.ms < 3e3, 2, `Status ${page.status}, ${page.ms} ms` + (page.redirected ? ", after a redirect" : ""), page.ok ? "The server took over 3 seconds to answer. Cache HTML at the edge and cut server work on the first byte." : "The URL did not return 200. Fix the response before anything else.");
      add("seo", "title", "Title tag present and 30 to 60 characters", title2 && title2.length >= 30 && title2.length <= 60, 6, title2 ? `"${title2}" (${title2.length} chars)` : "No title tag", !title2 ? "Add a title tag that leads with the primary keyword and ends with the brand." : title2.length > 60 ? "Shorten the title to 60 characters so Google does not truncate it." : "Lengthen the title to at least 30 characters and include the primary keyword.");
      add("seo", "desc", "Meta description 70 to 160 characters", desc && desc.length >= 70 && desc.length <= 160, 6, desc ? `${desc.length} chars` : "Missing", !desc ? "Write a 120 to 160 character meta description that states the outcome and includes the keyword." : desc.length > 160 ? "Trim the meta description to 160 characters." : "Expand the meta description to at least 70 characters with a clear benefit.");
      add("seo", "h1", "Exactly one H1", h1s.length === 1, 5, `${h1s.length} H1 tag${h1s.length === 1 ? "" : "s"}` + (h1s[0] ? `: "${h1s[0].text.slice(0, 80)}"` : ""), h1s.length === 0 ? "Add one H1 that states the page topic in plain words." : "Keep one H1 per page and demote the others to H2.");
      add("seo", "hier", "Heading levels do not skip", jumps === 0 && hs.length > 1, 3, `${hs.length} headings, ${jumps} level jump${jumps === 1 ? "" : "s"}`, "Fix heading order so H2 follows H1 and H3 follows H2. Screen readers and crawlers use the outline.");
      add("seo", "canonical", "Canonical URL set", !!canon, 5, canon || "Missing", 'Add <link rel="canonical"> pointing to the one URL you want indexed for this content.');
      add("seo", "viewport", "Mobile viewport meta", viewport, 3, viewport ? "Present" : "Missing", 'Add <meta name="viewport" content="width=device-width, initial-scale=1"> for mobile first indexing.');
      add("seo", "lang", "HTML lang attribute", lang, 1, lang ? "Present" : "Missing", 'Set <html lang="en"> (or the right language code).');
      add("seo", "alt", "Images carry alt text", imgs.length === 0 || imgsNoAlt / imgs.length <= 0.1, 4, `${imgs.length - imgsNoAlt} of ${imgs.length} images have alt`, `Add descriptive alt text to the ${imgsNoAlt} images missing it.`);
      add("seo", "robots", "robots.txt exists and does not block everything", robots.ok && !blocksAll && !robotsMeta.includes("noindex"), 4, robots.ok ? blocksAll ? "Disallow: / for all bots" : robotsMeta.includes("noindex") ? "Page has a noindex meta tag" : "OK" : `robots.txt returned ${robots.status || robots.error}`, blocksAll ? "Your robots.txt blocks every crawler. Remove the blanket Disallow." : robotsMeta.includes("noindex") ? "This page carries noindex. Remove it if the page should rank." : "Publish a robots.txt that allows crawling and lists your sitemap.");
      add("seo", "sitemap", "XML sitemap reachable", sitemap.ok && /<urlset|<sitemapindex/i.test(sitemap.text), 4, sitemap.ok ? "Found at /sitemap.xml" : `No sitemap at /sitemap.xml (${sitemap.status || sitemap.error})`, "Generate an XML sitemap at /sitemap.xml, reference it in robots.txt and submit it in Search Console.");
      add("seo", "og", "Open Graph title, description and image", og === 3, 3, `${og} of 3 tags`, "Add og:title, og:description and a 1200 by 630 og:image so shares render a card.");
      add("seo", "links", "At least 10 internal links", internal >= 10, 4, `${internal} internal links`, "Add contextual internal links to related pages so crawlers and readers can move through the site.");
      add("seo", "weight", "HTML under 500 KB with few inline scripts", sizeKb < 500 && inlineScripts <= 12, 2, `${sizeKb} KB HTML, ${inlineScripts} inline scripts`, "Trim the HTML payload and move scripts to cached external files.");
      add("seo", "words", "Enough body copy to rank (300+ words)", words >= 300, 3, `${words} words`, "Thin pages rarely rank. Add real copy that answers the search intent, aim for 600+ words.");
      add("aeo", "ld", "Valid JSON-LD structured data", ld.length > 0 && !invalidLd, 8, ld.length ? invalidLd ? "Present but one block does not parse" : [...types].slice(0, 6).join(", ") : "None found", invalidLd ? "One JSON-LD block has a syntax error. Validate it in the Rich Results Test." : "Add JSON-LD: WebSite, Organization or Person, and the page type (Article, Service, Product).");
      add("aeo", "entity", "Organization or Person entity declared", types.has("Organization") || types.has("Person") || types.has("ProfessionalService") || types.has("LocalBusiness"), 4, types.size ? `Types: ${[...types].slice(0, 8).join(", ")}` : "No entity schema", "Declare who publishes the site with Organization or Person schema, including sameAs links to LinkedIn and other profiles. Answer engines resolve entities, not pages.");
      add("aeo", "faq", "FAQ, HowTo or Article schema on the page", ["FAQPage", "HowTo", "Article", "BlogPosting", "NewsArticle", "TechArticle"].some((t) => types.has(t)), 6, "Question and answer schema tells engines exactly which text answers which question", "Add FAQPage schema with 4 to 6 real questions buyers ask, each answered in 40 to 60 words.");
      add("aeo", "llms", "llms.txt published", llms.ok && /^#|\n#/.test(llms.text) && llms.text.length > 100, 6, llms.ok ? "Found at /llms.txt" : "Not found at /llms.txt", "Publish /llms.txt: a markdown summary of who you are, what you offer and links to the pages worth citing.");
      add("aeo", "aibots", "AI crawlers allowed in robots.txt", robots.ok && blockedBots.length === 0, 6, blockedBots.length ? `Blocked: ${blockedBots.join(", ")}` : "GPTBot, ClaudeBot, PerplexityBot and Google-Extended can crawl", `Unblock ${blockedBots.join(", ")} in robots.txt or you cannot be cited by those assistants.`);
      add("aeo", "questions", "Question style headings or FAQ section", qHeads >= 2 || /faq|frequently asked/i.test(body), 4, `${qHeads} headings phrased as questions`, "Rewrite 2 or 3 H2s as the exact question a buyer types, and answer it in the first sentence below.");
      add("aeo", "answer", "Direct answer right under the H1 (40 to 80 words)", firstPara >= 40 && firstPara <= 90, 3, firstPara ? `${firstPara} words in the first paragraph` : "No paragraph found after the H1", "Open with a 40 to 80 word paragraph that answers the page question outright. That is the snippet AI engines lift.");
      add("aeo", "trust", "Author and dates visible to machines", hasAuthor && hasDates, 3, `${hasAuthor ? "Author found" : "No author"}, ${hasDates ? "dates found" : "no dates"}`, "Add an author with a profile link and datePublished or dateModified so engines can judge freshness and expertise.");
      const seo = checks.filter((c) => c.group === "seo").reduce((s, c) => s + c.points, 0);
      const aeo = checks.filter((c) => c.group === "aeo").reduce((s, c) => s + c.points, 0);
      const seoMax = checks.filter((c) => c.group === "seo").reduce((s, c) => s + c.max, 0);
      const aeoMax = checks.filter((c) => c.group === "aeo").reduce((s, c) => s + c.max, 0);
      return { checks, seo, aeo, seoMax, aeoMax, total: seo + aeo, title: title2, h1: h1s[0] ? h1s[0].text : "", words };
    }
    __name(score, "score");
    function drActions(dr) {
      if (!dr || !dr.connected || dr.rating == null) return [];
      const r = dr.rating;
      if (r < 10) return [{ priority: "high", group: "authority", label: `Domain Rating ${r}: almost no referring domains`, action: "Start with 10 to 15 easy links: partner pages, directories in your category, founder interviews, guest posts on peer blogs. Then publish one linkable asset a quarter (benchmark, calculator, original data)." }];
      if (r < 30) return [{ priority: "high", group: "authority", label: `Domain Rating ${r}: authority is the bottleneck`, action: "Rankings for competitive terms need DR 30+. Run a digital PR push around original data and get listed on comparison and alternatives pages in your category." }];
      if (r < 50) return [{ priority: "medium", group: "authority", label: `Domain Rating ${r}: solid base`, action: "Protect what you have (fix lost links, redirect dead pages) and earn links to money pages, not just the blog." }];
      return [{ priority: "low", group: "authority", label: `Domain Rating ${r}: strong profile`, action: "Authority is not your problem. Spend the effort on AEO: entity schema, llms.txt and question led content that AI engines can quote." }];
    }
    __name(drActions, "drActions");
    exports.handler = async function(event) {
      if (event.httpMethod !== "POST") return json2(405, { ok: false, error: "Use POST." });
      const ip = (event.headers["x-nf-client-connection-ip"] || event.headers["client-ip"] || "unknown").split(",")[0].trim();
      const now = Date.now();
      const cap = Number(process.env.SCORE_MAX_PER_10MIN || 6);
      const recent = (hits2.get(ip) || []).filter((t) => now - t < 6e5);
      if (recent.length >= cap) return json2(429, { ok: false, error: "Too many checks from this connection. Try again in a few minutes." });
      recent.push(now);
      hits2.set(ip, recent);
      let body;
      try {
        body = JSON.parse(event.body || "{}");
      } catch (e) {
        return json2(400, { ok: false, error: "Bad request." });
      }
      const u = normalizeUrl2(body.url);
      if (!u) return json2(400, { ok: false, error: "Enter a public website URL, like example.com." });
      const origin = u.origin;
      const [page, robots, sitemap, llms, dr] = await Promise.all([
        fetchText(u.href),
        fetchText(origin + "/robots.txt", { timeout: 6e3, max: 2e5, accept: "text/plain,*/*" }),
        fetchText(origin + "/sitemap.xml", { timeout: 6e3, max: 2e5, accept: "application/xml,text/xml,*/*" }),
        fetchText(origin + "/llms.txt", { timeout: 6e3, max: 2e5, accept: "text/plain,*/*" }),
        domainRating(u.hostname.replace(/^www\./, ""))
      ]);
      if (!page.text) return json2(422, { ok: false, error: page.error === "timeout" ? "The site took too long to answer." : `Could not fetch that page (${page.status || page.error}).` });
      if (!/<html|<head|<body|<title/i.test(page.text.slice(0, 5e3))) return json2(422, { ok: false, error: "That URL did not return an HTML page." });
      const s = score(page, robots, sitemap, llms, u);
      const actions = s.checks.filter((c) => !c.pass).map((c) => ({ priority: c.priority, group: c.group, label: c.label, action: c.action, detail: c.detail, impact: c.max })).concat(drActions(dr)).sort((a, b) => ({ high: 0, medium: 1, low: 2 })[a.priority] - { high: 0, medium: 1, low: 2 }[b.priority] || (b.impact || 0) - (a.impact || 0));
      return json2(200, {
        ok: true,
        url: u.href,
        finalUrl: page.url,
        fetchedAt: (/* @__PURE__ */ new Date()).toISOString(),
        page: { title: s.title, h1: s.h1, words: s.words, status: page.status, ms: page.ms },
        scores: { seo: s.seo, seoMax: s.seoMax, aeo: s.aeo, aeoMax: s.aeoMax, total: s.total, totalMax: s.seoMax + s.aeoMax },
        dr,
        checks: s.checks,
        actions
      });
    };
  }
});

// api/seo-aeo-score.js
var import_seo_aeo_score, onRequest3;
var init_seo_aeo_score = __esm({
  "api/seo-aeo-score.js"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    import_seo_aeo_score = __toESM(require_seo_aeo_score());
    init_platform();
    onRequest3 = v1(import_seo_aeo_score.default.handler);
  }
});

// medium-feed.js
async function onRequest4() {
  try {
    const r = await fetch(FEED, { headers: { "User-Agent": "syedcreates.com feed reader", Accept: "application/rss+xml,application/xml,text/xml" }, cf: { cacheTtl: 1800, cacheEverything: true } });
    return new Response(await r.text(), { status: r.status, headers: { "Content-Type": "application/xml; charset=utf-8", "Cache-Control": "public, max-age=1800" } });
  } catch (e) {
    return new Response('<?xml version="1.0"?><rss version="2.0"><channel></channel></rss>', { status: 502, headers: { "Content-Type": "application/xml" } });
  }
}
var FEED;
var init_medium_feed = __esm({
  "medium-feed.js"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    FEED = "https://medium.com/feed/@ssyedhadi";
    __name(onRequest4, "onRequest");
  }
});

// _middleware.js
function futureSlugs(now) {
  return Object.keys(SCHEDULE).filter((s) => now < Date.parse(SCHEDULE[s]));
}
function withHeaders(res, cache) {
  const h = new Headers(res.headers);
  h.set("Cache-Control", cache);
  h.delete("Content-Length");
  return h;
}
async function onRequest5(ctx) {
  const url = new URL(ctx.request.url);
  const now = ctx.env.SCHEDULE_NOW ? Date.parse(ctx.env.SCHEDULE_NOW) : Date.now();
  const future = futureSlugs(now);
  if (!future.length) return ctx.next();
  const path = url.pathname.replace(/\/+$/, "") || "/";
  const slug = path.slice(1).replace(/\.html$/, "");
  try {
    if (future.includes(slug)) {
      const nf = await ctx.env.ASSETS.fetch(new URL("/404.html", url));
      return new Response(nf.body, { status: 404, headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" } });
    }
    const res = await ctx.next();
    if (res.status !== 200) return res;
    if (path === "/blog" || path === "/blog.html") {
      const out = new HTMLRewriter().on("[data-pub]", {
        element(el) {
          if (now < Date.parse(el.getAttribute("data-pub"))) el.remove();
        }
      }).transform(res);
      return new Response(out.body, { status: 200, headers: withHeaders(res, "public, max-age=0, must-revalidate") });
    }
    let text = await res.text();
    if (path === "/sitemap.xml") {
      for (const s of future) text = text.replace(new RegExp("\\s*<url><loc>https://syedcreates\\.com/" + s + "</loc>.*?</url>", "g"), "");
    } else if (path === "/llms-full.txt") {
      text = text.split("\n---\n").filter((sec) => !future.some((s) => sec.includes("URL: https://syedcreates.com/" + s + "\n") || sec.trimEnd().endsWith("URL: https://syedcreates.com/" + s))).join("\n---\n");
    } else if (path === "/llms.txt") {
      text = text.split("\n").filter((l) => !future.some((s) => l.includes("syedcreates.com/" + s + ")"))).join("\n");
    } else if (path === "/assets/search-index.json") {
      const data = JSON.parse(text);
      data.pages = data.pages.filter((p) => !future.includes(String(p.u || "").replace(/^\//, "")));
      text = JSON.stringify(data);
    }
    return new Response(text, { status: 200, headers: withHeaders(res, "public, max-age=300") });
  } catch (e) {
    return ctx.next();
  }
}
var SCHEDULE;
var init_middleware = __esm({
  "_middleware.js"() {
    init_functionsRoutes_0_4960377568767962();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
    init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
    init_performance2();
    SCHEDULE = {
      "gtm-plays-behind-0-to-10m": "2026-11-10T03:30:00Z",
      "ai-search-cnapp-240-percent": "2026-11-17T03:30:00Z",
      "fire-math-epf-ppf-nps": "2026-11-19T03:30:00Z",
      "one-line-positioning-test": "2026-11-24T03:30:00Z",
      "partner-programs-that-ship-pipeline": "2026-12-01T03:30:00Z",
      "2m-pipeline-100k-budget": "2026-12-08T03:30:00Z",
      "23-content-types-5-that-sold": "2026-12-15T03:30:00Z",
      "salary-in-2046": "2026-12-17T03:30:00Z",
      "gtm-lessons-from-leaders-2026": "2026-12-22T03:30:00Z",
      "0-to-10m-10-lessons": "2026-12-29T03:30:00Z"
    };
    __name(futureSlugs, "futureSlugs");
    __name(withHeaders, "withHeaders");
    __name(onRequest5, "onRequest");
  }
});

// ../.wrangler/tmp/pages-jm4rBl/functionsRoutes-0.4960377568767962.mjs
var routes;
var init_functionsRoutes_0_4960377568767962 = __esm({
  "../.wrangler/tmp/pages-jm4rBl/functionsRoutes-0.4960377568767962.mjs"() {
    init_company_research();
    init_salary_report();
    init_seo_aeo_score();
    init_medium_feed();
    init_middleware();
    routes = [
      {
        routePath: "/api/company-research",
        mountPath: "/api",
        method: "",
        middlewares: [],
        modules: [onRequest]
      },
      {
        routePath: "/api/salary-report",
        mountPath: "/api",
        method: "",
        middlewares: [],
        modules: [onRequest2]
      },
      {
        routePath: "/api/seo-aeo-score",
        mountPath: "/api",
        method: "",
        middlewares: [],
        modules: [onRequest3]
      },
      {
        routePath: "/medium-feed",
        mountPath: "/",
        method: "",
        middlewares: [],
        modules: [onRequest4]
      },
      {
        routePath: "/",
        mountPath: "/",
        method: "",
        middlewares: [onRequest5],
        modules: []
      }
    ];
  }
});

// ../.wrangler/tmp/bundle-xVfjuz/middleware-loader.entry.ts
init_functionsRoutes_0_4960377568767962();
init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
init_performance2();

// ../.wrangler/tmp/bundle-xVfjuz/middleware-insertion-facade.js
init_functionsRoutes_0_4960377568767962();
init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
init_performance2();

// ../../wr/node_modules/wrangler/templates/pages-template-worker.ts
init_functionsRoutes_0_4960377568767962();
init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
init_performance2();

// ../../wr/node_modules/path-to-regexp/dist.es2015/index.js
init_functionsRoutes_0_4960377568767962();
init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
init_performance2();
function lexer(str) {
  var tokens = [];
  var i = 0;
  while (i < str.length) {
    var char = str[i];
    if (char === "*" || char === "+" || char === "?") {
      tokens.push({ type: "MODIFIER", index: i, value: str[i++] });
      continue;
    }
    if (char === "\\") {
      tokens.push({ type: "ESCAPED_CHAR", index: i++, value: str[i++] });
      continue;
    }
    if (char === "{") {
      tokens.push({ type: "OPEN", index: i, value: str[i++] });
      continue;
    }
    if (char === "}") {
      tokens.push({ type: "CLOSE", index: i, value: str[i++] });
      continue;
    }
    if (char === ":") {
      var name = "";
      var j = i + 1;
      while (j < str.length) {
        var code = str.charCodeAt(j);
        if (
          // `0-9`
          code >= 48 && code <= 57 || // `A-Z`
          code >= 65 && code <= 90 || // `a-z`
          code >= 97 && code <= 122 || // `_`
          code === 95
        ) {
          name += str[j++];
          continue;
        }
        break;
      }
      if (!name)
        throw new TypeError("Missing parameter name at ".concat(i));
      tokens.push({ type: "NAME", index: i, value: name });
      i = j;
      continue;
    }
    if (char === "(") {
      var count3 = 1;
      var pattern = "";
      var j = i + 1;
      if (str[j] === "?") {
        throw new TypeError('Pattern cannot start with "?" at '.concat(j));
      }
      while (j < str.length) {
        if (str[j] === "\\") {
          pattern += str[j++] + str[j++];
          continue;
        }
        if (str[j] === ")") {
          count3--;
          if (count3 === 0) {
            j++;
            break;
          }
        } else if (str[j] === "(") {
          count3++;
          if (str[j + 1] !== "?") {
            throw new TypeError("Capturing groups are not allowed at ".concat(j));
          }
        }
        pattern += str[j++];
      }
      if (count3)
        throw new TypeError("Unbalanced pattern at ".concat(i));
      if (!pattern)
        throw new TypeError("Missing pattern at ".concat(i));
      tokens.push({ type: "PATTERN", index: i, value: pattern });
      i = j;
      continue;
    }
    tokens.push({ type: "CHAR", index: i, value: str[i++] });
  }
  tokens.push({ type: "END", index: i, value: "" });
  return tokens;
}
__name(lexer, "lexer");
function parse(str, options) {
  if (options === void 0) {
    options = {};
  }
  var tokens = lexer(str);
  var _a = options.prefixes, prefixes = _a === void 0 ? "./" : _a, _b = options.delimiter, delimiter = _b === void 0 ? "/#?" : _b;
  var result = [];
  var key = 0;
  var i = 0;
  var path = "";
  var tryConsume = /* @__PURE__ */ __name(function(type) {
    if (i < tokens.length && tokens[i].type === type)
      return tokens[i++].value;
  }, "tryConsume");
  var mustConsume = /* @__PURE__ */ __name(function(type) {
    var value2 = tryConsume(type);
    if (value2 !== void 0)
      return value2;
    var _a2 = tokens[i], nextType = _a2.type, index = _a2.index;
    throw new TypeError("Unexpected ".concat(nextType, " at ").concat(index, ", expected ").concat(type));
  }, "mustConsume");
  var consumeText = /* @__PURE__ */ __name(function() {
    var result2 = "";
    var value2;
    while (value2 = tryConsume("CHAR") || tryConsume("ESCAPED_CHAR")) {
      result2 += value2;
    }
    return result2;
  }, "consumeText");
  var isSafe = /* @__PURE__ */ __name(function(value2) {
    for (var _i = 0, delimiter_1 = delimiter; _i < delimiter_1.length; _i++) {
      var char2 = delimiter_1[_i];
      if (value2.indexOf(char2) > -1)
        return true;
    }
    return false;
  }, "isSafe");
  var safePattern = /* @__PURE__ */ __name(function(prefix2) {
    var prev = result[result.length - 1];
    var prevText = prefix2 || (prev && typeof prev === "string" ? prev : "");
    if (prev && !prevText) {
      throw new TypeError('Must have text between two parameters, missing text after "'.concat(prev.name, '"'));
    }
    if (!prevText || isSafe(prevText))
      return "[^".concat(escapeString(delimiter), "]+?");
    return "(?:(?!".concat(escapeString(prevText), ")[^").concat(escapeString(delimiter), "])+?");
  }, "safePattern");
  while (i < tokens.length) {
    var char = tryConsume("CHAR");
    var name = tryConsume("NAME");
    var pattern = tryConsume("PATTERN");
    if (name || pattern) {
      var prefix = char || "";
      if (prefixes.indexOf(prefix) === -1) {
        path += prefix;
        prefix = "";
      }
      if (path) {
        result.push(path);
        path = "";
      }
      result.push({
        name: name || key++,
        prefix,
        suffix: "",
        pattern: pattern || safePattern(prefix),
        modifier: tryConsume("MODIFIER") || ""
      });
      continue;
    }
    var value = char || tryConsume("ESCAPED_CHAR");
    if (value) {
      path += value;
      continue;
    }
    if (path) {
      result.push(path);
      path = "";
    }
    var open = tryConsume("OPEN");
    if (open) {
      var prefix = consumeText();
      var name_1 = tryConsume("NAME") || "";
      var pattern_1 = tryConsume("PATTERN") || "";
      var suffix = consumeText();
      mustConsume("CLOSE");
      result.push({
        name: name_1 || (pattern_1 ? key++ : ""),
        pattern: name_1 && !pattern_1 ? safePattern(prefix) : pattern_1,
        prefix,
        suffix,
        modifier: tryConsume("MODIFIER") || ""
      });
      continue;
    }
    mustConsume("END");
  }
  return result;
}
__name(parse, "parse");
function match(str, options) {
  var keys = [];
  var re = pathToRegexp(str, keys, options);
  return regexpToFunction(re, keys, options);
}
__name(match, "match");
function regexpToFunction(re, keys, options) {
  if (options === void 0) {
    options = {};
  }
  var _a = options.decode, decode = _a === void 0 ? function(x) {
    return x;
  } : _a;
  return function(pathname) {
    var m = re.exec(pathname);
    if (!m)
      return false;
    var path = m[0], index = m.index;
    var params = /* @__PURE__ */ Object.create(null);
    var _loop_1 = /* @__PURE__ */ __name(function(i2) {
      if (m[i2] === void 0)
        return "continue";
      var key = keys[i2 - 1];
      if (key.modifier === "*" || key.modifier === "+") {
        params[key.name] = m[i2].split(key.prefix + key.suffix).map(function(value) {
          return decode(value, key);
        });
      } else {
        params[key.name] = decode(m[i2], key);
      }
    }, "_loop_1");
    for (var i = 1; i < m.length; i++) {
      _loop_1(i);
    }
    return { path, index, params };
  };
}
__name(regexpToFunction, "regexpToFunction");
function escapeString(str) {
  return str.replace(/([.+*?=^!:${}()[\]|/\\])/g, "\\$1");
}
__name(escapeString, "escapeString");
function flags(options) {
  return options && options.sensitive ? "" : "i";
}
__name(flags, "flags");
function regexpToRegexp(path, keys) {
  if (!keys)
    return path;
  var groupsRegex = /\((?:\?<(.*?)>)?(?!\?)/g;
  var index = 0;
  var execResult = groupsRegex.exec(path.source);
  while (execResult) {
    keys.push({
      // Use parenthesized substring match if available, index otherwise
      name: execResult[1] || index++,
      prefix: "",
      suffix: "",
      modifier: "",
      pattern: ""
    });
    execResult = groupsRegex.exec(path.source);
  }
  return path;
}
__name(regexpToRegexp, "regexpToRegexp");
function arrayToRegexp(paths, keys, options) {
  var parts = paths.map(function(path) {
    return pathToRegexp(path, keys, options).source;
  });
  return new RegExp("(?:".concat(parts.join("|"), ")"), flags(options));
}
__name(arrayToRegexp, "arrayToRegexp");
function stringToRegexp(path, keys, options) {
  return tokensToRegexp(parse(path, options), keys, options);
}
__name(stringToRegexp, "stringToRegexp");
function tokensToRegexp(tokens, keys, options) {
  if (options === void 0) {
    options = {};
  }
  var _a = options.strict, strict = _a === void 0 ? false : _a, _b = options.start, start2 = _b === void 0 ? true : _b, _c = options.end, end = _c === void 0 ? true : _c, _d = options.encode, encode = _d === void 0 ? function(x) {
    return x;
  } : _d, _e = options.delimiter, delimiter = _e === void 0 ? "/#?" : _e, _f = options.endsWith, endsWith = _f === void 0 ? "" : _f;
  var endsWithRe = "[".concat(escapeString(endsWith), "]|$");
  var delimiterRe = "[".concat(escapeString(delimiter), "]");
  var route = start2 ? "^" : "";
  for (var _i = 0, tokens_1 = tokens; _i < tokens_1.length; _i++) {
    var token = tokens_1[_i];
    if (typeof token === "string") {
      route += escapeString(encode(token));
    } else {
      var prefix = escapeString(encode(token.prefix));
      var suffix = escapeString(encode(token.suffix));
      if (token.pattern) {
        if (keys)
          keys.push(token);
        if (prefix || suffix) {
          if (token.modifier === "+" || token.modifier === "*") {
            var mod3 = token.modifier === "*" ? "?" : "";
            route += "(?:".concat(prefix, "((?:").concat(token.pattern, ")(?:").concat(suffix).concat(prefix, "(?:").concat(token.pattern, "))*)").concat(suffix, ")").concat(mod3);
          } else {
            route += "(?:".concat(prefix, "(").concat(token.pattern, ")").concat(suffix, ")").concat(token.modifier);
          }
        } else {
          if (token.modifier === "+" || token.modifier === "*") {
            throw new TypeError('Can not repeat "'.concat(token.name, '" without a prefix and suffix'));
          }
          route += "(".concat(token.pattern, ")").concat(token.modifier);
        }
      } else {
        route += "(?:".concat(prefix).concat(suffix, ")").concat(token.modifier);
      }
    }
  }
  if (end) {
    if (!strict)
      route += "".concat(delimiterRe, "?");
    route += !options.endsWith ? "$" : "(?=".concat(endsWithRe, ")");
  } else {
    var endToken = tokens[tokens.length - 1];
    var isEndDelimited = typeof endToken === "string" ? delimiterRe.indexOf(endToken[endToken.length - 1]) > -1 : endToken === void 0;
    if (!strict) {
      route += "(?:".concat(delimiterRe, "(?=").concat(endsWithRe, "))?");
    }
    if (!isEndDelimited) {
      route += "(?=".concat(delimiterRe, "|").concat(endsWithRe, ")");
    }
  }
  return new RegExp(route, flags(options));
}
__name(tokensToRegexp, "tokensToRegexp");
function pathToRegexp(path, keys, options) {
  if (path instanceof RegExp)
    return regexpToRegexp(path, keys);
  if (Array.isArray(path))
    return arrayToRegexp(path, keys, options);
  return stringToRegexp(path, keys, options);
}
__name(pathToRegexp, "pathToRegexp");

// ../../wr/node_modules/wrangler/templates/pages-template-worker.ts
var escapeRegex = /[.+?^${}()|[\]\\]/g;
function getOriginalPathPrefix(requestPath, normalizedPrefix) {
  let end = 0;
  for (let index = 0; index < normalizedPrefix.length; index++) {
    end++;
    if (normalizedPrefix[index] === "/") {
      while (requestPath[end] === "/") {
        end++;
      }
    }
  }
  return requestPath.slice(0, end);
}
__name(getOriginalPathPrefix, "getOriginalPathPrefix");
function* executeRequest(request) {
  const requestPath = new URL(request.url).pathname;
  const normalizedRequestPath = requestPath.replace(/\/+/g, "/");
  for (const route of [...routes].reverse()) {
    if (route.method && route.method !== request.method) {
      continue;
    }
    const routeMatcher = match(route.routePath.replace(escapeRegex, "\\$&"), {
      end: false
    });
    const mountMatcher = match(route.mountPath.replace(escapeRegex, "\\$&"), {
      end: false
    });
    const matchResult = routeMatcher(requestPath) || routeMatcher(normalizedRequestPath);
    const originalMountMatch = mountMatcher(requestPath);
    const mountMatchResult = originalMountMatch || mountMatcher(normalizedRequestPath);
    if (matchResult && mountMatchResult) {
      const path = originalMountMatch ? originalMountMatch.path : getOriginalPathPrefix(requestPath, mountMatchResult.path);
      for (const handler of route.middlewares.flat()) {
        yield {
          handler,
          params: matchResult.params,
          path
        };
      }
    }
  }
  for (const route of routes) {
    if (route.method && route.method !== request.method) {
      continue;
    }
    const routeMatcher = match(route.routePath.replace(escapeRegex, "\\$&"), {
      end: true
    });
    const mountMatcher = match(route.mountPath.replace(escapeRegex, "\\$&"), {
      end: false
    });
    const matchResult = routeMatcher(requestPath);
    const mountMatchResult = mountMatcher(requestPath);
    if (matchResult && mountMatchResult && route.modules.length) {
      for (const handler of route.modules.flat()) {
        yield {
          handler,
          params: matchResult.params,
          path: matchResult.path
        };
      }
      break;
    }
  }
}
__name(executeRequest, "executeRequest");
var pages_template_worker_default = {
  async fetch(originalRequest, env2, workerContext) {
    let request = originalRequest;
    const handlerIterator = executeRequest(request);
    let data = {};
    let isFailOpen = false;
    const next = /* @__PURE__ */ __name(async (input, init) => {
      if (input !== void 0) {
        let url = input;
        if (typeof input === "string") {
          url = new URL(input, request.url).toString();
        }
        request = new Request(url, init);
      }
      const result = handlerIterator.next();
      if (result.done === false) {
        const { handler, params, path } = result.value;
        const context2 = {
          request: new Request(request.clone()),
          functionPath: path,
          next,
          params,
          get data() {
            return data;
          },
          set data(value) {
            if (typeof value !== "object" || value === null) {
              throw new Error("context.data must be an object");
            }
            data = value;
          },
          env: env2,
          waitUntil: workerContext.waitUntil.bind(workerContext),
          passThroughOnException: /* @__PURE__ */ __name(() => {
            isFailOpen = true;
          }, "passThroughOnException")
        };
        const response = await handler(context2);
        if (!(response instanceof Response)) {
          throw new Error("Your Pages function should return a Response");
        }
        return cloneResponse(response);
      } else if ("ASSETS") {
        const response = await env2["ASSETS"].fetch(request);
        return cloneResponse(response);
      } else {
        const response = await fetch(request);
        return cloneResponse(response);
      }
    }, "next");
    try {
      return await next();
    } catch (error3) {
      if (isFailOpen) {
        const response = await env2["ASSETS"].fetch(request);
        return cloneResponse(response);
      }
      throw error3;
    }
  }
};
var cloneResponse = /* @__PURE__ */ __name((response) => (
  // https://fetch.spec.whatwg.org/#null-body-status
  new Response(
    [101, 204, 205, 304].includes(response.status) ? null : response.body,
    response
  )
), "cloneResponse");

// ../../wr/node_modules/wrangler/templates/middleware/middleware-ensure-req-body-drained.ts
init_functionsRoutes_0_4960377568767962();
init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
init_performance2();
var drainBody = /* @__PURE__ */ __name(async (request, env2, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env2);
  } finally {
    try {
      if (request.body !== null && !request.bodyUsed) {
        const reader = request.body.getReader();
        while (!(await reader.read()).done) {
        }
      }
    } catch (e) {
      console.error("Failed to drain the unused request body.", e);
    }
  }
}, "drainBody");
var middleware_ensure_req_body_drained_default = drainBody;

// ../../wr/node_modules/wrangler/templates/middleware/middleware-miniflare3-json-error.ts
init_functionsRoutes_0_4960377568767962();
init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
init_performance2();
function reduceError(e) {
  return {
    name: e?.name,
    message: e?.message ?? String(e),
    stack: e?.stack,
    cause: e?.cause === void 0 ? void 0 : reduceError(e.cause)
  };
}
__name(reduceError, "reduceError");
var jsonError = /* @__PURE__ */ __name(async (request, env2, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env2);
  } catch (e) {
    const error3 = reduceError(e);
    const body = JSON.stringify(error3);
    const headers = {
      "Content-Type": "application/json",
      "MF-Experimental-Error-Stack": "true"
    };
    const encoded = encodeURIComponent(body);
    if (encoded.length <= 8192) {
      headers["MF-Experimental-Error-Stack-Payload"] = encoded;
    }
    return new Response(body, { status: 500, headers });
  }
}, "jsonError");
var middleware_miniflare3_json_error_default = jsonError;

// ../.wrangler/tmp/bundle-xVfjuz/middleware-insertion-facade.js
var __INTERNAL_WRANGLER_MIDDLEWARE__ = [
  middleware_ensure_req_body_drained_default,
  middleware_miniflare3_json_error_default
];
var middleware_insertion_facade_default = pages_template_worker_default;

// ../../wr/node_modules/wrangler/templates/middleware/common.ts
init_functionsRoutes_0_4960377568767962();
init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_process();
init_virtual_unenv_global_polyfill_cloudflare_unenv_preset_node_console();
init_performance2();
var __facade_middleware__ = [];
function __facade_register__(...args) {
  __facade_middleware__.push(...args.flat());
}
__name(__facade_register__, "__facade_register__");
function __facade_invokeChain__(request, env2, ctx, dispatch, middlewareChain) {
  const [head, ...tail] = middlewareChain;
  const middlewareCtx = {
    dispatch,
    next(newRequest, newEnv) {
      return __facade_invokeChain__(newRequest, newEnv, ctx, dispatch, tail);
    }
  };
  return head(request, env2, ctx, middlewareCtx);
}
__name(__facade_invokeChain__, "__facade_invokeChain__");
function __facade_invoke__(request, env2, ctx, dispatch, finalMiddleware) {
  return __facade_invokeChain__(request, env2, ctx, dispatch, [
    ...__facade_middleware__,
    finalMiddleware
  ]);
}
__name(__facade_invoke__, "__facade_invoke__");

// ../.wrangler/tmp/bundle-xVfjuz/middleware-loader.entry.ts
var __Facade_ScheduledController__ = class ___Facade_ScheduledController__ {
  constructor(scheduledTime, cron, noRetry) {
    this.scheduledTime = scheduledTime;
    this.cron = cron;
    this.#noRetry = noRetry;
  }
  scheduledTime;
  cron;
  static {
    __name(this, "__Facade_ScheduledController__");
  }
  #noRetry;
  noRetry() {
    if (!(this instanceof ___Facade_ScheduledController__)) {
      throw new TypeError("Illegal invocation");
    }
    this.#noRetry();
  }
};
function wrapExportedHandler(worker) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return worker;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  const fetchDispatcher = /* @__PURE__ */ __name(function(request, env2, ctx) {
    if (worker.fetch === void 0) {
      throw new Error("Handler does not export a fetch() function.");
    }
    return worker.fetch(request, env2, ctx);
  }, "fetchDispatcher");
  return {
    ...worker,
    fetch(request, env2, ctx) {
      const dispatcher = /* @__PURE__ */ __name(function(type, init) {
        if (type === "scheduled" && worker.scheduled !== void 0) {
          const controller = new __Facade_ScheduledController__(
            Date.now(),
            init.cron ?? "",
            () => {
            }
          );
          return worker.scheduled(controller, env2, ctx);
        }
      }, "dispatcher");
      return __facade_invoke__(request, env2, ctx, dispatcher, fetchDispatcher);
    }
  };
}
__name(wrapExportedHandler, "wrapExportedHandler");
function wrapWorkerEntrypoint(klass) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return klass;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  return class extends klass {
    #fetchDispatcher = /* @__PURE__ */ __name((request, env2, ctx) => {
      this.env = env2;
      this.ctx = ctx;
      if (super.fetch === void 0) {
        throw new Error("Entrypoint class does not define a fetch() function.");
      }
      return super.fetch(request);
    }, "#fetchDispatcher");
    #dispatcher = /* @__PURE__ */ __name((type, init) => {
      if (type === "scheduled" && super.scheduled !== void 0) {
        const controller = new __Facade_ScheduledController__(
          Date.now(),
          init.cron ?? "",
          () => {
          }
        );
        return super.scheduled(controller);
      }
    }, "#dispatcher");
    fetch(request) {
      return __facade_invoke__(
        request,
        this.env,
        this.ctx,
        this.#dispatcher,
        this.#fetchDispatcher
      );
    }
  };
}
__name(wrapWorkerEntrypoint, "wrapWorkerEntrypoint");
var WRAPPED_ENTRY;
if (typeof middleware_insertion_facade_default === "object") {
  WRAPPED_ENTRY = wrapExportedHandler(middleware_insertion_facade_default);
} else if (typeof middleware_insertion_facade_default === "function") {
  WRAPPED_ENTRY = wrapWorkerEntrypoint(middleware_insertion_facade_default);
}
var middleware_loader_entry_default = WRAPPED_ENTRY;
export {
  __INTERNAL_WRANGLER_MIDDLEWARE__,
  middleware_loader_entry_default as default
};
//# sourceMappingURL=functionsWorker-0.12304600587687653.mjs.map
