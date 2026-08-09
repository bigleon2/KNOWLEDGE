module.exports = [
"[externals]/fs [external] (fs, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("fs", () => require("fs"));

module.exports = mod;
}),
"[externals]/next/dist/compiled/@opentelemetry/api [external] (next/dist/compiled/@opentelemetry/api, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/compiled/@opentelemetry/api", () => require("next/dist/compiled/@opentelemetry/api"));

module.exports = mod;
}),
"[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[externals]/next/dist/compiled/next-server/app-route-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-route-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/compiled/next-server/app-route-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-route-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/action-async-storage.external.js [external] (next/dist/server/app-render/action-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/server/app-render/action-async-storage.external.js", () => require("next/dist/server/app-render/action-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/after-task-async-storage.external.js [external] (next/dist/server/app-render/after-task-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/server/app-render/after-task-async-storage.external.js", () => require("next/dist/server/app-render/after-task-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-async-storage.external.js [external] (next/dist/server/app-render/work-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/server/app-render/work-async-storage.external.js", () => require("next/dist/server/app-render/work-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-unit-async-storage.external.js [external] (next/dist/server/app-render/work-unit-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/server/app-render/work-unit-async-storage.external.js", () => require("next/dist/server/app-render/work-unit-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/runtime-reacts.external.js [external] (next/dist/server/runtime-reacts.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/server/runtime-reacts.external.js", () => require("next/dist/server/runtime-reacts.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/shared/lib/no-fallback-error.external.js [external] (next/dist/shared/lib/no-fallback-error.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/shared/lib/no-fallback-error.external.js", () => require("next/dist/shared/lib/no-fallback-error.external.js"));

module.exports = mod;
}),
"[externals]/node:stream [external] (node:stream, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("node:stream", () => require("node:stream"));

module.exports = mod;
}),
"[externals]/path [external] (path, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("path", () => require("path"));

module.exports = mod;
}),
"[project]/src/app/api/skills/relations/route.ts [app-route] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "GET",
    ()=>GET
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/server.js [app-route] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$skills$2d$reader$2e$ts__$5b$app$2d$route$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/skills-reader.ts [app-route] (ecmascript)");
;
;
async function GET() {
    try {
        const skills = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$skills$2d$reader$2e$ts__$5b$app$2d$route$5d$__$28$ecmascript$29$__["getAllSkills"])();
        const relations = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$skills$2d$reader$2e$ts__$5b$app$2d$route$5d$__$28$ecmascript$29$__["getRelations"])();
        const nodes = skills.map((s)=>({
                id: s.slug,
                name: s.name,
                category: s.category,
                version: s.version,
                language: s.language,
                tags: s.tags,
                dependencies: s.dependencies
            }));
        return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json({
            nodes,
            edges: relations
        });
    } catch (error) {
        console.error('Error reading relations:', error);
        return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json({
            error: 'Failed to read relations'
        }, {
            status: 500
        });
    }
}
}),
"[project]/src/lib/skills-reader.ts [app-route] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "getAllSkills",
    ()=>getAllSkills,
    "getRelations",
    ()=>getRelations,
    "getSkillBySlug",
    ()=>getSkillBySlug,
    "getSkillsStats",
    ()=>getSkillsStats
]);
var __TURBOPACK__imported__module__$5b$externals$5d2f$fs__$5b$external$5d$__$28$fs$2c$__cjs$29$__ = __turbopack_context__.i("[externals]/fs [external] (fs, cjs)");
var __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__ = __turbopack_context__.i("[externals]/path [external] (path, cjs)");
;
;
const SKILLS_ROOT = __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__["default"].join(process.cwd(), 'skills');
// Ecosystem skill names (those with category: ecosystem or known by convention)
const ECOSYSTEM_SKILLS = new Set([
    'gen-plan',
    'correct-work',
    'clone-chat',
    'skills-inventory',
    'skill-creator',
    'autonomous-agent',
    'task-review'
]);
function parseFrontmatter(content) {
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) return {};
    try {
        // Simple YAML-like parser (not a full YAML parser, but handles our formats)
        const yaml = match[1];
        const result = {};
        let currentKey = '';
        let currentList = [];
        let inList = false;
        let currentObj = null;
        let currentObjKey = '';
        let inObj = false;
        const lines = yaml.split('\n');
        for (const line of lines){
            // List item
            const listMatch = line.match(/^\s+-\s+(.+)/);
            if (listMatch) {
                if (inObj && currentObj) {
                    // Inside an object, list items are values of the last key
                    const val = listMatch[1].replace(/^['"]|['"]$/g, '').trim();
                    currentList.push(val);
                    currentObj[currentObjKey] = [
                        ...currentList
                    ];
                } else if (inList) {
                    currentList.push(listMatch[1].replace(/^['"]|['"]$/g, '').trim());
                    result[currentKey] = [
                        ...currentList
                    ];
                }
                continue;
            }
            // Nested object key (e.g., "  author: Z.AI")
            const nestedMatch = line.match(/^\s+(\w[\w-]*):\s*(.*)/);
            if (nestedMatch && inObj && currentObj) {
                const key = nestedMatch[1];
                const val = nestedMatch[2].replace(/^['"]|['"]$/g, '').trim();
                if (val) {
                    currentObj[key] = val;
                    currentList = [];
                    currentObjKey = key;
                    inList = false;
                } else {
                    currentList = [];
                    currentObjKey = key;
                    inList = true;
                }
                continue;
            }
            // Top-level key
            const keyMatch = line.match(/^(\w[\w-]*):\s*(.*)/);
            if (keyMatch) {
                // Save previous
                if (inObj && currentObj) {
                    result[currentKey] = currentObj;
                } else if (inList) {
                    result[currentKey] = [
                        ...currentList
                    ];
                }
                currentKey = keyMatch[1];
                const val = keyMatch[2].replace(/^['"]|['"]$/g, '').trim();
                if (val === '' || val === '|' || val === '>') {
                    // Could be a list or object below
                    inList = true;
                    currentList = [];
                    inObj = true;
                    currentObj = {};
                    currentObjKey = '';
                } else {
                    result[currentKey] = val;
                    inList = false;
                    inObj = false;
                    currentObj = null;
                }
                continue;
            }
        }
        // Save last
        if (inObj && currentObj) {
            result[currentKey] = currentObj;
        } else if (inList) {
            result[currentKey] = [
                ...currentList
            ];
        }
        return result;
    } catch  {
        return {};
    }
}
function extractDescription(content, frontmatter) {
    // Try to get description from frontmatter first
    let desc = '';
    const fm = frontmatter;
    if (typeof fm.description === 'string') {
        desc = fm.description;
    }
    // If no frontmatter description, extract from body (first non-heading paragraph)
    if (!desc) {
        const body = content.replace(/^---[\s\S]*?---\n/, '');
        const lines = body.split('\n').filter((l)=>l.trim() && !l.startsWith('#'));
        desc = lines.slice(0, 3).join(' ').trim();
    }
    const full = desc;
    const short = desc.length > 200 ? desc.slice(0, 200) + '...' : desc;
    return {
        short,
        full
    };
}
function getFileType(filePath) {
    const dir = __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__["default"].dirname(filePath).split('/').pop() || '';
    const ext = __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__["default"].extname(filePath);
    if (filePath.endsWith('SKILL.md')) return 'skill';
    if (dir === 'scripts' || dir === 'mini-services') return 'script';
    if (dir === 'references') return 'reference';
    if (dir === 'evals') return 'eval';
    if (dir === 'assets' || dir === 'data' || [
        '.png',
        '.jpg',
        '.svg',
        '.ico',
        '.csv'
    ].includes(ext)) return 'asset';
    return 'other';
}
function walkDir(dir, base) {
    const files = [];
    try {
        const entries = __TURBOPACK__imported__module__$5b$externals$5d2f$fs__$5b$external$5d$__$28$fs$2c$__cjs$29$__["default"].readdirSync(dir, {
            withFileTypes: true
        });
        for (const entry of entries){
            const full = __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__["default"].join(dir, entry.name);
            if (entry.name.startsWith('.') || entry.name === 'node_modules' || entry.name === '__pycache__') continue;
            if (entry.isDirectory()) {
                files.push(...walkDir(full, base));
            } else {
                try {
                    files.push({
                        path: __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__["default"].relative(base, full),
                        size: __TURBOPACK__imported__module__$5b$externals$5d2f$fs__$5b$external$5d$__$28$fs$2c$__cjs$29$__["default"].statSync(full).size
                    });
                } catch  {
                // skip unreadable
                }
            }
        }
    } catch  {
    // skip
    }
    return files;
}
function getAllSkills() {
    const dirs = __TURBOPACK__imported__module__$5b$externals$5d2f$fs__$5b$external$5d$__$28$fs$2c$__cjs$29$__["default"].readdirSync(SKILLS_ROOT, {
        withFileTypes: true
    }).filter((d)=>d.isDirectory() && !d.name.startsWith('.') && d.name !== 'node_modules' && d.name !== '__pycache__').map((d)=>d.name).sort();
    return dirs.map((slug)=>{
        const skillPath = __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__["default"].join(SKILLS_ROOT, slug, 'SKILL.md');
        const content = __TURBOPACK__imported__module__$5b$externals$5d2f$fs__$5b$external$5d$__$28$fs$2c$__cjs$29$__["default"].existsSync(skillPath) ? __TURBOPACK__imported__module__$5b$externals$5d2f$fs__$5b$external$5d$__$28$fs$2c$__cjs$29$__["default"].readFileSync(skillPath, 'utf-8') : '';
        const fm = parseFrontmatter(content);
        const { short, full } = extractDescription(content, fm);
        // Extract version from various formats
        let version = '—';
        const meta = fm.metadata;
        if (typeof fm.version === 'string') version = fm.version;
        else if (meta && typeof meta.version === 'string') version = meta.version;
        else if (meta && typeof meta.version === 'number') version = String(meta.version);
        // Determine category
        let category = ECOSYSTEM_SKILLS.has(slug) ? 'ecosystem' : 'metier';
        if (typeof fm.category === 'string') {
            if (fm.category === 'ecosystem' || fm.category === 'écosystème') category = 'ecosystem';
            else if (fm.category === 'metier' || fm.category === 'métier') category = 'metier';
        }
        // Language
        const language = typeof fm.language === 'string' ? fm.language : short.match(/[\u4e00-\u9fff]/) ? 'zh' : 'en';
        // Tags
        let tags = [];
        if (Array.isArray(fm.tags)) tags = fm.tags.filter((t)=>typeof t === 'string');
        if (typeof fm.tags === 'string') tags = fm.tags.split(',').map((t)=>t.trim()).filter(Boolean);
        // Dependencies
        let dependencies = [];
        if (Array.isArray(fm.dependencies)) dependencies = fm.dependencies.filter((t)=>typeof t === 'string');
        if (typeof fm.dependencies === 'string') dependencies = fm.dependencies.split(',').map((t)=>t.trim()).filter(Boolean);
        // Directory analysis
        const skillDir = __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__["default"].join(SKILLS_ROOT, slug);
        const files = walkDir(skillDir, SKILLS_ROOT);
        const fileCount = files.length;
        const totalSize = files.reduce((s, f)=>s + f.size, 0);
        const hasReferences = files.some((f)=>getFileType(f.path) === 'reference');
        const hasScripts = files.some((f)=>getFileType(f.path) === 'script');
        const hasEvals = files.some((f)=>getFileType(f.path) === 'eval');
        return {
            name: typeof fm.name === 'string' ? fm.name : slug,
            slug,
            version,
            category,
            language,
            description: short,
            tags,
            dependencies,
            hasReferences,
            hasScripts,
            hasEvals,
            fileCount,
            totalSize,
            contentPreview: full
        };
    });
}
function getSkillBySlug(slug) {
    const skillDir = __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__["default"].join(SKILLS_ROOT, slug);
    const skillPath = __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__["default"].join(skillDir, 'SKILL.md');
    if (!__TURBOPACK__imported__module__$5b$externals$5d2f$fs__$5b$external$5d$__$28$fs$2c$__cjs$29$__["default"].existsSync(skillPath)) return null;
    const content = __TURBOPACK__imported__module__$5b$externals$5d2f$fs__$5b$external$5d$__$28$fs$2c$__cjs$29$__["default"].readFileSync(skillPath, 'utf-8');
    const fm = parseFrontmatter(content);
    const { short, full } = extractDescription(content, fm);
    let version = '—';
    const meta = fm.metadata;
    if (typeof fm.version === 'string') version = fm.version;
    else if (meta && typeof meta.version === 'string') version = meta.version;
    let category = ECOSYSTEM_SKILLS.has(slug) ? 'ecosystem' : 'metier';
    if (typeof fm.category === 'string') {
        if (fm.category === 'ecosystem' || fm.category === 'écosystème') category = 'ecosystem';
        else category = 'metier';
    }
    const language = typeof fm.language === 'string' ? fm.language : short.match(/[\u4e00-\u9fff]/) ? 'zh' : 'en';
    let tags = [];
    if (Array.isArray(fm.tags)) tags = fm.tags.filter((t)=>typeof t === 'string');
    if (typeof fm.tags === 'string') tags = fm.tags.split(',').map((t)=>t.trim()).filter(Boolean);
    let dependencies = [];
    if (Array.isArray(fm.dependencies)) dependencies = fm.dependencies.filter((t)=>typeof t === 'string');
    if (typeof fm.dependencies === 'string') dependencies = fm.dependencies.split(',').map((t)=>t.trim()).filter(Boolean);
    const files = walkDir(skillDir, SKILLS_ROOT).map((f)=>({
            ...f,
            type: getFileType(f.path)
        }));
    const fileCount = files.length;
    const totalSize = files.reduce((s, f)=>s + f.size, 0);
    const hasReferences = files.some((f)=>f.type === 'reference');
    const hasScripts = files.some((f)=>f.type === 'script');
    const hasEvals = files.some((f)=>f.type === 'eval');
    return {
        name: typeof fm.name === 'string' ? fm.name : slug,
        slug,
        version,
        category,
        language,
        description: short,
        tags,
        dependencies,
        hasReferences,
        hasScripts,
        hasEvals,
        fileCount,
        totalSize,
        contentPreview: full,
        fullDescription: full,
        files
    };
}
function getSkillsStats() {
    const skills = getAllSkills();
    const ecosystem = skills.filter((s)=>s.category === 'ecosystem');
    const metier = skills.filter((s)=>s.category === 'metier');
    const languages = {};
    skills.forEach((s)=>{
        languages[s.language] = (languages[s.language] || 0) + 1;
    });
    const totalFiles = skills.reduce((s, sk)=>s + sk.fileCount, 0);
    const totalSize = skills.reduce((s, sk)=>s + sk.totalSize, 0);
    const withRefs = skills.filter((s)=>s.hasReferences).length;
    const withScripts = skills.filter((s)=>s.hasScripts).length;
    const withEvals = skills.filter((s)=>s.hasEvals).length;
    const withDeps = skills.filter((s)=>s.dependencies.length > 0).length;
    const withTags = skills.filter((s)=>s.tags.length > 0).length;
    // Build dependency graph
    const depGraph = {};
    skills.forEach((s)=>{
        if (s.dependencies.length > 0) depGraph[s.slug] = s.dependencies;
    });
    return {
        total: skills.length,
        ecosystem: ecosystem.length,
        metier: metier.length,
        languages,
        totalFiles,
        totalSize,
        withReferences: withRefs,
        withScripts,
        withEvals,
        withDeps,
        withTags,
        dependencyGraph: depGraph
    };
}
function getRelations() {
    // Build relations from dependencies + known ecosystem relationships
    const skills = getAllSkills();
    const relations = [];
    const slugMap = {};
    skills.forEach((s)=>{
        slugMap[s.slug] = s.name;
    });
    // Dependency relations
    skills.forEach((s)=>{
        s.dependencies.forEach((dep)=>{
            // Normalize dep name to slug
            const depSlug = dep.toLowerCase().replace(/[\s_]+/g, '-');
            relations.push({
                source: s.slug,
                target: depSlug,
                type: 'depends_on'
            });
            relations.push({
                source: depSlug,
                target: s.slug,
                type: 'used_by'
            });
        });
    });
    // Known ecosystem relations (from KNOWLEDGE.md conventions)
    const knownRelations = [
        [
            'gen-plan',
            'correct-work'
        ],
        [
            'gen-plan',
            'clone-chat'
        ],
        [
            'correct-work',
            'gen-plan'
        ],
        [
            'correct-work',
            'clone-chat'
        ],
        [
            'skills-inventory',
            'autonomous-agent'
        ],
        [
            'skill-creator',
            'skills-inventory'
        ],
        [
            'task-review',
            'skill-creator'
        ],
        [
            'autonomous-agent',
            'gen-plan'
        ],
        [
            'autonomous-agent',
            'correct-work'
        ]
    ];
    knownRelations.forEach(([a, b])=>{
        if (slugMap[a] && slugMap[b]) {
            const exists = relations.some((r)=>r.source === a && r.target === b || r.source === b && r.target === a);
            if (!exists) {
                relations.push({
                    source: a,
                    target: b,
                    type: 'related'
                });
            }
        }
    });
    // Deduplicate
    const seen = new Set();
    return relations.filter((r)=>{
        const key = [
            r.source,
            r.target,
            r.type
        ].join('→');
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
    });
}
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__1-isakv._.js.map