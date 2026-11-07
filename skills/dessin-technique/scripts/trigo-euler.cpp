// ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.28)
// SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
// Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (R4)
// Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
//
// dessin-technique — nœud C++ trigo-euler (v1.0.0, Task 58 — G2-SG2.1).
//
// Moteur mathématique déterministe du skill dessin-technique (voie géométrique) :
// trigonométrie, équations canoniques (cercle, ellipse), analyse (dérivée,
// primitive, intégrale), séries de Fourier, théorème d'Euler (formule, rotation,
// projection isométrique CAO, caractéristique), géométrie des pièces (profil
// axial 2D, modèle isométrique flat-shaded).
//
// Contrat : skills/inter-scripts/scripts/registre.json (v1.0.0 — source de vérité)
//   binaire   : skills/dessin-technique/scripts/trigo-euler
//   source    : skills/dessin-technique/scripts/trigo-euler.cpp
//   compilation (EXACTE) : g++ -O2 -std=c++17 -pthread -Wall trigo-euler.cpp -o trigo-euler
//   interface : json-ndjson — requête {"op": "...", "args": {...}}
//   modes     : one-shot (--request F --out F) | stdin (NDJSON) | daemon (--daemon)
//   daemon    : --socket /tmp/trigo-euler.sock --ready-file /tmp/trigo-euler.ready
//               --pid-file /tmp/trigo-euler.pid --max-clients 8
//   capacites : trig.eval, trig.resoudre, canonique.cercle, canonique.ellipse,
//     analyse.derivee, analyse.primitive, analyse.integrale, fourier.serie,
//     fourier.eval, euler.formule, euler.rotation, euler.projection,
//     euler.caracteristique, piece.profil_2d, piece.modele_iso
//     + echo (health-check) + daemon.stop (arrêt propre)
//   saturation : 9e connexion avec 8 clients actifs -> {"ok":false,"erreur":"daemon sature"}
//                (refus NON-BLOQUANT : réponse immédiate puis fermeture)
//
// Enseignements de conception intégrés (discussions d'origine — voir plan Task 58
// §0-bis E13-5/6/7) : ratio d'ellipse par VALEURS SINGULIÈRES (le ratio bbox d'une
// ellipse inclinée est faux) ; vérification mécanique ratio caps ≈ sin(élévation) ;
// Gauss-Legendre 5 points (tolérance 1e-6) ; painter iso = liste de rendu UNIFIÉE
// (faces + traits) TRIÉE par profondeur ; caps dessinés seulement si visibles
// (n·dir > 0) ; arcs de cap en moitié externe (échantillonnage par normales
// visibles) ; silhouette par ARÊTES LOCALES (chaque jonction résolue par ses deux
// segments adjacents — jamais de résolution globale) ; polygone fermé (gorge
// O-ring) ; formatage FRANÇAIS des cotes (Ø, mm, virgule décimale, N·m) ;
// déterminisme intégral (sorties %.10g, ordre d'insertion stable — idempotence R3).
//
// Domaine d'usage (VOSS COOLING, session d'origine du skill) : pièces de révolution
// filetées (raccords hydrauliques — joint 5c : cotes F1 officielles 44,9 × 35,2 mm,
// filet G Ø 28,5 × 22,7, O-ring 22,7→23,9, hexagone entre-pointes 35,2 × 23,9→33,8,
// filet D 34,5→41,9, bores Ø 15,4/12,0/6,0 ; couples 40/120 N·m).

#include <algorithm>
#include <atomic>
#include <cerrno>
#include <cmath>
#include <csignal>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <functional>
#include <iostream>
#include <sstream>
#include <string>
#include <thread>
#include <utility>
#include <vector>

#include <poll.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

static const char* VERSION_SCRIPT = "1.0.0";
static const double PI = 3.14159265358979323846;
// Élévation isométrique CAO standard : atan(1/√2) ≈ 35,264389682754654°
static const double ISO_ELEV_DEG = 35.264389682754654;

static double deg2rad(double d) { return d * PI / 180.0; }
static double rad2deg(double r) { return r * 180.0 / PI; }

// ============================ Mini-JSON (ordonné) ============================

struct JVal {
    enum Type { NUL, BOO, NUM, STR, ARR, OBJ };
    Type t = NUL;
    bool b = false;
    double num = 0.0;
    std::string str;
    std::vector<JVal> arr;
    std::vector<std::pair<std::string, JVal>> obj;  // ordre d'insertion préservé

    static JVal nul() { return JVal(); }
    static JVal boo(bool v) { JVal j; j.t = BOO; j.b = v; return j; }
    static JVal nombre(double v) { JVal j; j.t = NUM; j.num = v; return j; }
    static JVal texte(const std::string& v) { JVal j; j.t = STR; j.str = v; return j; }
    static JVal tableau() { JVal j; j.t = ARR; return j; }
    static JVal objet() { JVal j; j.t = OBJ; return j; }

    bool has(const std::string& k) const {
        if (t != OBJ) return false;
        for (const auto& p : obj) if (p.first == k) return true;
        return false;
    }
    const JVal* get(const std::string& k) const {
        if (t != OBJ) return nullptr;
        for (const auto& p : obj) if (p.first == k) return &p.second;
        return nullptr;
    }
    JVal& set(const std::string& k, JVal v) {
        for (auto& p : obj) if (p.first == k) { p.second = std::move(v); return p.second; }
        obj.emplace_back(k, std::move(v));
        return obj.back().second;
    }
    double get_num(const std::string& k, double def) const {
        const JVal* j = get(k);
        return (j && j->t == NUM) ? j->num : def;
    }
    std::string get_str(const std::string& k, const std::string& def) const {
        const JVal* j = get(k);
        return (j && j->t == STR) ? j->str : def;
    }
    bool get_boo(const std::string& k, bool def) const {
        const JVal* j = get(k);
        return (j && j->t == BOO) ? j->b : def;
    }
};

static std::string fmt_nombre(double v) {
    // Déterminisme : entiers exacts -> forme entière, sinon %.10g.
    if (v == 0.0) return "0";  // éradique -0
    if (std::floor(v) == v && std::fabs(v) < 1e15) {
        char buf[32];
        std::snprintf(buf, sizeof buf, "%lld", static_cast<long long>(v));
        return buf;
    }
    char buf[40];
    std::snprintf(buf, sizeof buf, "%.10g", v);
    return buf;
}

static std::string jval_dump(const JVal& j) {
    switch (j.t) {
        case JVal::NUL: return "null";
        case JVal::BOO: return j.b ? "true" : "false";
        case JVal::NUM: return fmt_nombre(j.num);
        case JVal::STR: {
            std::string out = "\"";
            for (unsigned char c : j.str) {
                switch (c) {
                    case '"': out += "\\\""; break;
                    case '\\': out += "\\\\"; break;
                    case '\n': out += "\\n"; break;
                    case '\r': out += "\\r"; break;
                    case '\t': out += "\\t"; break;
                    default:
                        if (c < 0x20) {
                            char buf[8];
                            std::snprintf(buf, sizeof buf, "\\u%04x", c);
                            out += buf;
                        } else {
                            out += static_cast<char>(c);  // UTF-8 pass-through
                        }
                }
            }
            out += "\"";
            return out;
        }
        case JVal::ARR: {
            std::string out = "[";
            for (size_t i = 0; i < j.arr.size(); ++i) {
                if (i) out += ",";
                out += jval_dump(j.arr[i]);
            }
            return out + "]";
        }
        case JVal::OBJ: {
            std::string out = "{";
            for (size_t i = 0; i < j.obj.size(); ++i) {
                if (i) out += ",";
                out += "\"" + j.obj[i].first + "\":" + jval_dump(j.obj[i].second);
            }
            return out + "}";
        }
    }
    return "null";
}

struct JsonParseError {
    std::string message;
    size_t position;
};

static void utf8_encode(unsigned cp, std::string& out) {
    if (cp < 0x80) {
        out += static_cast<char>(cp);
    } else if (cp < 0x800) {
        out += static_cast<char>(0xC0 | (cp >> 6));
        out += static_cast<char>(0x80 | (cp & 0x3F));
    } else {
        out += static_cast<char>(0xE0 | (cp >> 12));
        out += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
        out += static_cast<char>(0x80 | (cp & 0x3F));
    }
}

class Parser {
public:
    explicit Parser(const std::string& s) : s_(s) {}

    bool parse(JVal& out, std::string& err) {
        try {
            i_ = 0;
            sauter_blancs();
            if (i_ >= s_.size()) throw Err("entrée vide");
            out = valeur();
            sauter_blancs();
            if (i_ < s_.size()) throw Err("contenu superflu après la valeur");
            return true;
        } catch (const Err& e) {
            err = e.msg + " (position " + std::to_string(i_) + ")";
            return false;
        }
    }

private:
    struct Err { std::string msg; Err(std::string m) : msg(std::move(m)) {} };
    const std::string& s_;
    size_t i_ = 0;

    void sauter_blancs() {
        while (i_ < s_.size() && (s_[i_] == ' ' || s_[i_] == '\t' || s_[i_] == '\r' ||
                                  s_[i_] == '\n'))
            ++i_;
    }
    char peek() {
        if (i_ >= s_.size()) throw Err("fin prématurée");
        return s_[i_];
    }
    void attendu(char c) {
        if (i_ >= s_.size() || s_[i_] != c)
            throw Err(std::string("caractère attendu '") + c + "'");
        ++i_;
    }
    JVal valeur() {
        char c = peek();
        if (c == '{') return objet();
        if (c == '[') return tableau();
        if (c == '"') return JVal::texte(chaine());
        if (c == 't' || c == 'f' || c == 'n') return mot();
        return nombre();
    }
    JVal objet() {
        attendu('{');
        JVal j = JVal::objet();
        sauter_blancs();
        if (peek() == '}') { ++i_; return j; }
        while (true) {
            sauter_blancs();
            std::string cle = chaine();
            sauter_blancs();
            attendu(':');
            sauter_blancs();
            j.obj.emplace_back(cle, valeur());
            sauter_blancs();
            char d = peek();
            if (d == ',') { ++i_; continue; }
            if (d == '}') { ++i_; break; }
            throw Err("',' ou '}' attendu");
        }
        return j;
    }
    JVal tableau() {
        attendu('[');
        JVal j = JVal::tableau();
        sauter_blancs();
        if (peek() == ']') { ++i_; return j; }
        while (true) {
            sauter_blancs();
            j.arr.push_back(valeur());
            sauter_blancs();
            char d = peek();
            if (d == ',') { ++i_; continue; }
            if (d == ']') { ++i_; break; }
            throw Err("',' ou ']' attendu");
        }
        return j;
    }
    std::string chaine() {
        attendu('"');
        std::string out;
        while (true) {
            if (i_ >= s_.size()) throw Err("chaîne non terminée");
            char c = s_[i_++];
            if (c == '"') break;
            if (c == '\\') {
                if (i_ >= s_.size()) throw Err("échappement incomplet");
                char e = s_[i_++];
                switch (e) {
                    case '"': out += '"'; break;
                    case '\\': out += '\\'; break;
                    case '/': out += '/'; break;
                    case 'n': out += '\n'; break;
                    case 'r': out += '\r'; break;
                    case 't': out += '\t'; break;
                    case 'b': out += '\b'; break;
                    case 'f': out += '\f'; break;
                    case 'u': {
                        if (i_ + 4 > s_.size()) throw Err("\\uXXXX incomplet");
                        unsigned cp = 0;
                        for (int k = 0; k < 4; ++k) {
                            char h = s_[i_++];
                            cp <<= 4;
                            if (h >= '0' && h <= '9') cp += static_cast<unsigned>(h - '0');
                            else if (h >= 'a' && h <= 'f') cp += static_cast<unsigned>(h - 'a' + 10);
                            else if (h >= 'A' && h <= 'F') cp += static_cast<unsigned>(h - 'A' + 10);
                            else throw Err("hexadécimal invalide");
                        }
                        // paires de substitution UTF-16
                        if (cp >= 0xD800 && cp <= 0xDBFF && i_ + 6 <= s_.size() &&
                            s_[i_] == '\\' && s_[i_ + 1] == 'u') {
                            unsigned lo = 0;
                            size_t save = i_;
                            i_ += 2;
                            bool ok = true;
                            for (int k = 0; k < 4; ++k) {
                                char h = s_[i_++];
                                lo <<= 4;
                                if (h >= '0' && h <= '9') lo += static_cast<unsigned>(h - '0');
                                else if (h >= 'a' && h <= 'f') lo += static_cast<unsigned>(h - 'a' + 10);
                                else if (h >= 'A' && h <= 'F') lo += static_cast<unsigned>(h - 'A' + 10);
                                else { ok = false; break; }
                            }
                            if (ok && lo >= 0xDC00 && lo <= 0xDFFF) {
                                cp = 0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00);
                            } else {
                                i_ = save;  // surrogate isolé : encodé tel quel
                            }
                        }
                        utf8_encode(cp, out);
                        break;
                    }
                    default: throw Err("échappement inconnu");
                }
            } else {
                out += c;  // UTF-8 pass-through
            }
        }
        return out;
    }
    JVal mot() {
        if (s_.compare(i_, 4, "true") == 0) { i_ += 4; return JVal::boo(true); }
        if (s_.compare(i_, 5, "false") == 0) { i_ += 5; return JVal::boo(false); }
        if (s_.compare(i_, 4, "null") == 0) { i_ += 4; return JVal::nul(); }
        throw Err("littéral invalide");
    }
    JVal nombre() {
        size_t debut = i_;
        if (i_ < s_.size() && (s_[i_] == '-' || s_[i_] == '+')) ++i_;
        while (i_ < s_.size() && ((s_[i_] >= '0' && s_[i_] <= '9') || s_[i_] == '.' ||
                                  s_[i_] == 'e' || s_[i_] == 'E' || s_[i_] == '-' ||
                                  s_[i_] == '+'))
            ++i_;
        if (i_ == debut) throw Err("valeur invalide");
        std::string frag = s_.substr(debut, i_ - debut);
        errno = 0;
        char* fin = nullptr;
        double v = std::strtod(frag.c_str(), &fin);
        if (fin == frag.c_str() || errno == ERANGE) throw Err("nombre invalide : " + frag);
        return JVal::nombre(v);
    }
};

static bool json_parse(const std::string& texte, JVal& out, std::string& err) {
    Parser p(texte);
    return p.parse(out, err);
}

// ============================ Formatage français ============================

// Cote française : virgule décimale, zéros traînants supprimés ("44,9" pas "44,90").
static std::string fmt_fr(double v, int decimales = 2) {
    if (std::fabs(v) < 5e-13) v = 0.0;
    char buf[64];
    std::snprintf(buf, sizeof buf, "%.*f", decimales, v);
    std::string s(buf);
    if (s.find('.') != std::string::npos) {
        while (!s.empty() && s.back() == '0') s.pop_back();
        if (!s.empty() && s.back() == '.') s.pop_back();
        if (s.empty() || s == "-") s = "0";
    }
    for (auto& c : s)
        if (c == '.') c = ',';
    return s;
}

// ============================ Algèbre linéaire ============================

struct Vec3 {
    double x = 0, y = 0, z = 0;
    Vec3() = default;
    Vec3(double a, double b, double c) : x(a), y(b), z(c) {}
    double dot(const Vec3& o) const { return x * o.x + y * o.y + z * o.z; }
    Vec3 cross(const Vec3& o) const {
        return Vec3(y * o.z - z * o.y, z * o.x - x * o.z, x * o.y - y * o.x);
    }
    double norme() const { return std::sqrt(dot(*this)); }
    Vec3 normalise() const {
        double n = norme();
        return n > 1e-15 ? Vec3(x / n, y / n, z / n) : Vec3(0, 0, 0);
    }
};

struct Mat3 {
    double m[3][3] = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};
    static Mat3 identite() {
        Mat3 r;
        r.m[0][0] = r.m[1][1] = r.m[2][2] = 1;
        return r;
    }
    Vec3 ligne(int i) const { return Vec3(m[i][0], m[i][1], m[i][2]); }
    Vec3 colonne(int j) const { return Vec3(m[0][j], m[1][j], m[2][j]); }
    Vec3 applique(const Vec3& v) const {
        return Vec3(m[0][0] * v.x + m[0][1] * v.y + m[0][2] * v.z,
                    m[1][0] * v.x + m[1][1] * v.y + m[1][2] * v.z,
                    m[2][0] * v.x + m[2][1] * v.y + m[2][2] * v.z);
    }
    Mat3 multiplie(const Mat3& o) const {
        Mat3 r;
        for (int i = 0; i < 3; ++i)
            for (int j = 0; j < 3; ++j)
                r.m[i][j] = m[i][0] * o.m[0][j] + m[i][1] * o.m[1][j] + m[i][2] * o.m[2][j];
        return r;
    }
    double trace() const { return m[0][0] + m[1][1] + m[2][2]; }
    double determinant() const {
        return m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) -
               m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) +
               m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]);
    }
};

static Mat3 rotation_x(double a) {
    Mat3 r = Mat3::identite();
    double c = std::cos(a), s = std::sin(a);
    r.m[1][1] = c; r.m[1][2] = -s; r.m[2][1] = s; r.m[2][2] = c;
    return r;
}
static Mat3 rotation_y(double a) {
    Mat3 r = Mat3::identite();
    double c = std::cos(a), s = std::sin(a);
    r.m[0][0] = c; r.m[0][2] = s; r.m[1][1] = 1; r.m[2][0] = -s; r.m[2][2] = c;
    return r;
}
static Mat3 rotation_z(double a) {
    Mat3 r = Mat3::identite();
    double c = std::cos(a), s = std::sin(a);
    r.m[0][0] = c; r.m[0][1] = -s; r.m[1][0] = s; r.m[1][1] = c;
    return r;
}

// Système linéaire N×N par élimination de Gauss avec pivot partiel.
// Retourne false si singulier. A est modifié (copie interne).
static bool gauss_resoudre(std::vector<std::vector<double>> a,
                           std::vector<double> b, std::vector<double>& x) {
    size_t n = a.size();
    for (size_t col = 0; col < n; ++col) {
        size_t piv = col;
        for (size_t r = col + 1; r < n; ++r)
            if (std::fabs(a[r][col]) > std::fabs(a[piv][col])) piv = r;
        if (std::fabs(a[piv][col]) < 1e-13) return false;
        std::swap(a[piv], a[col]);
        std::swap(b[piv], b[col]);
        for (size_t r = col + 1; r < n; ++r) {
            double f = a[r][col] / a[col][col];
            for (size_t c = col; c < n; ++c) a[r][c] -= f * a[col][c];
            b[r] -= f * b[col];
        }
    }
    x.assign(n, 0.0);
    for (size_t i = n; i-- > 0;) {
        double s = b[i];
        for (size_t c = i + 1; c < n; ++c) s -= a[i][c] * x[c];
        x[i] = s / a[i][i];
    }
    return true;
}

// Valeurs propres d'une matrice symétrique 2×2 [[a, b], [b, c]] (triées décroissantes).
static void eig2_sym(double a, double b, double c, double& l1, double& l2) {
    double tr = a + c;
    double disc = std::sqrt(std::max(0.0, (a - c) * (a - c) / 4.0 + b * b));
    l1 = tr / 2.0 + disc;
    l2 = tr / 2.0 - disc;
}

// Valeurs singulières d'une application linéaire 2×2 (lignes u,v ; colonnes x,y)
// — par valeurs propres de MᵀM. ENSEIGNEMENT D'ORIGINE : le ratio bbox d'une
// ellipse inclinée est FAUX ; le vrai petit axe = plus petite valeur singulière.
static void sv2(double m00, double m01, double m10, double m11,
                double& s1, double& s2) {
    double a = m00 * m00 + m10 * m10;
    double b = m00 * m01 + m10 * m11;
    double c = m01 * m01 + m11 * m11;
    double l1, l2;
    eig2_sym(a, b, c, l1, l2);
    s1 = std::sqrt(std::max(0.0, l1));
    s2 = std::sqrt(std::max(0.0, l2));
}

// Quaternion depuis une matrice de rotation (voie de Shepperd — stable à θ≈π).
static void quaternion_depuis_mat3(const Mat3& R, double q[4]) {
    double tr = R.trace();
    if (tr > 0.0) {
        double s = std::sqrt(tr + 1.0) * 2.0;
        q[0] = 0.25 * s;
        q[1] = (R.m[2][1] - R.m[1][2]) / s;
        q[2] = (R.m[0][2] - R.m[2][0]) / s;
        q[3] = (R.m[1][0] - R.m[0][1]) / s;
    } else if (R.m[0][0] > R.m[1][1] && R.m[0][0] > R.m[2][2]) {
        double s = std::sqrt(1.0 + R.m[0][0] - R.m[1][1] - R.m[2][2]) * 2.0;
        q[0] = (R.m[2][1] - R.m[1][2]) / s;
        q[1] = 0.25 * s;
        q[2] = (R.m[0][1] + R.m[1][0]) / s;
        q[3] = (R.m[0][2] + R.m[2][0]) / s;
    } else if (R.m[1][1] > R.m[2][2]) {
        double s = std::sqrt(1.0 + R.m[1][1] - R.m[0][0] - R.m[2][2]) * 2.0;
        q[0] = (R.m[0][2] - R.m[2][0]) / s;
        q[1] = (R.m[0][1] + R.m[1][0]) / s;
        q[2] = 0.25 * s;
        q[3] = (R.m[1][2] + R.m[2][1]) / s;
    } else {
        double s = std::sqrt(1.0 + R.m[2][2] - R.m[0][0] - R.m[1][1]) * 2.0;
        q[0] = (R.m[1][0] - R.m[0][1]) / s;
        q[1] = (R.m[0][2] + R.m[2][0]) / s;
        q[2] = (R.m[1][2] + R.m[2][1]) / s;
        q[3] = 0.25 * s;
    }
}

// ============================ Fonctions nommées ============================

static bool eval_fonction(const std::string& nom, double x, double y,
                          bool degres, double& resultat) {
    double xr = degres ? deg2rad(x) : x;
    double v;
    if (nom == "sin") v = std::sin(xr);
    else if (nom == "cos") v = std::cos(xr);
    else if (nom == "tan") v = std::tan(xr);
    else if (nom == "asin") {
        if (x < -1.0 || x > 1.0) return false;
        v = std::asin(x);
        if (degres) v = rad2deg(v);
    } else if (nom == "acos") {
        if (x < -1.0 || x > 1.0) return false;
        v = std::acos(x);
        if (degres) v = rad2deg(v);
    } else if (nom == "atan") {
        v = std::atan(x);
        if (degres) v = rad2deg(v);
    } else if (nom == "atan2") {
        v = std::atan2(x, y);
        if (degres) v = rad2deg(v);
    } else if (nom == "sinh") v = std::sinh(x);
    else if (nom == "cosh") v = std::cosh(x);
    else if (nom == "tanh") v = std::tanh(x);
    else if (nom == "exp") v = std::exp(x);
    else if (nom == "ln") {
        if (x <= 0.0) return false;
        v = std::log(x);
    } else if (nom == "log10") {
        if (x <= 0.0) return false;
        v = std::log10(x);
    } else if (nom == "sqrt") {
        if (x < 0.0) return false;
        v = std::sqrt(x);
    } else if (nom == "cbrt") v = std::cbrt(x);
    else if (nom == "abs") v = std::fabs(x);
    else if (nom == "plancher") v = std::floor(x);
    else if (nom == "plafond") v = std::ceil(x);
    else if (nom == "arrondi") v = std::round(x);
    else return false;
    resultat = v;
    return true;
}

// ============================ Intégration numérique ============================

// Gauss-Legendre 5 points sur [a, b] — tolérance visée 1e-6 (enseignement d'origine).
static double gauss5(std::function<double(double)> f, double a, double b) {
    static const double x[5] = {-0.9061798459386640, -0.5384693101056831, 0.0,
                                 0.5384693101056831, 0.9061798459386640};
    static const double w[5] = {0.2369268850561891, 0.4786286704993665,
                                0.5688888888888889, 0.4786286704993665,
                                0.2369268850561891};
    double demi = (b - a) / 2.0, mid = (a + b) / 2.0, s = 0.0;
    for (int i = 0; i < 5; ++i) s += w[i] * f(mid + demi * x[i]);
    return s * demi;
}

static double gauss5_compose(std::function<double(double)> f, double a, double b,
                             int intervalles) {
    if (intervalles < 1) intervalles = 1;
    double h = (b - a) / intervalles, s = 0.0;
    for (int i = 0; i < intervalles; ++i)
        s += gauss5(f, a + i * h, a + (i + 1) * h);
    return s;
}

// ============================ Projection isométrique ============================

struct Iso {
    double az = deg2rad(45.0);
    double el = deg2rad(ISO_ELEV_DEG);
    Vec3 dir{0, 0, 0};    // centre -> caméra
    Vec3 right{0, 0, 0};  // axe écran u
    Vec3 up{0, 0, 0};     // axe écran v (+z monde vers le haut de l'écran)

    Iso(double az_deg, double el_deg) {
        az = deg2rad(az_deg);
        el = deg2rad(el_deg);
        dir = Vec3(std::cos(el) * std::cos(az), std::cos(el) * std::sin(az), std::sin(el));
        right = Vec3(-std::sin(az), std::cos(az), 0.0);
        up = dir.cross(right);  // = (-sin el·cos az, -sin el·sin az, cos el)
    }
    double u(const Vec3& p) const { return p.dot(right); }
    double v(const Vec3& p) const { return p.dot(up); }
    double profondeur(const Vec3& p) const { return p.dot(dir); }  // grand = proche
    // Ratio du petit axe d'un cercle du plan horizontal, par VALEURS SINGULIÈRES
    // de la sous-application (lignes u,v ; colonnes x,y) — vérification mécanique
    // du respect de la perspective (théorique : sin(élévation)).
    double ratio_cap() const {
        double s1, s2;
        sv2(right.x, right.y, up.x, up.y, s1, s2);
        return (s1 > 1e-15) ? s2 / s1 : 0.0;
    }
};

// ============================ Opérations (15 capacités) ============================

static const char* CAPACITES[] = {
    "trig.eval", "trig.resoudre", "canonique.cercle", "canonique.ellipse",
    "analyse.derivee", "analyse.primitive", "analyse.integrale", "fourier.serie",
    "fourier.eval", "euler.formule", "euler.rotation", "euler.projection",
    "euler.caracteristique", "piece.profil_2d", "piece.modele_iso"};

static JVal liste_capacites() {
    JVal a = JVal::tableau();
    for (const char* c : CAPACITES) a.arr.push_back(JVal::texte(c));
    a.arr.push_back(JVal::texte("echo"));
    a.arr.push_back(JVal::texte("daemon.stop"));
    return a;
}

// Petit lecteur de points [[x, y], ...]
static bool lire_points_xy(const JVal& args, const std::string& cle,
                           std::vector<std::pair<double, double>>& pts,
                           size_t min_pts, std::string& err) {
    const JVal* a = args.get(cle);
    if (!a || a->t != JVal::ARR || a->arr.size() < min_pts) {
        err = "'" + cle + "' : tableau de " + std::to_string(min_pts) +
              " points [x, y] minimum requis";
        return false;
    }
    for (const JVal& p : a->arr) {
        if (p.t != JVal::ARR || p.arr.size() < 2 || p.arr[0].t != JVal::NUM ||
            p.arr[1].t != JVal::NUM) {
            err = "'" + cle + "' : chaque point doit être [x, y] numérique";
            return false;
        }
        pts.emplace_back(p.arr[0].num, p.arr[1].num);
    }
    return true;
}

// ---- trig.eval ----
static bool op_trig_eval(const JVal& args, JVal& out, std::string& err) {
    std::string f = args.get_str("fonction", "");
    if (f.empty()) { err = "'fonction' requis (sin, cos, tan, asin, acos, atan, atan2, sinh, cosh, tanh, exp, ln, log10, sqrt, cbrt, abs, plancher, plafond, arrondi)"; return false; }
    if (!args.has("x")) { err = "'x' requis (numérique)"; return false; }
    double x = args.get_num("x", 0.0), y = args.get_num("y", 0.0);
    bool degres = args.get_str("unites", "rad") == "deg";
    double v;
    if (!eval_fonction(f, x, y, degres, v)) {
        err = "fonction '" + f + "' inconnue ou hors domaine (x=" + fmt_fr(x) + ")";
        return false;
    }
    out.set("fonction", JVal::texte(f));
    out.set("x", JVal::nombre(x));
    out.set("unites", JVal::texte(degres ? "deg" : "rad"));
    out.set("valeur", JVal::nombre(v));
    return true;
}

// ---- trig.resoudre (triangle rectangle) ----
static bool op_trig_resoudre(const JVal& args, JVal& out, std::string& err) {
    bool hH = args.has("hypotenuse"), hO = args.has("oppose"), hA = args.has("adjacente"),
         hAng = args.has("angle_deg");
    double H = args.get_num("hypotenuse", 0.0), O = args.get_num("oppose", 0.0),
           A = args.get_num("adjacente", 0.0), an = args.get_num("angle_deg", 0.0);
    if (hH && args.get("hypotenuse")->t != JVal::NUM) hH = false;
    if (hO && args.get("oppose")->t != JVal::NUM) hO = false;
    if (hA && args.get("adjacente")->t != JVal::NUM) hA = false;
    if (hAng && args.get("angle_deg")->t != JVal::NUM) hAng = false;
    std::string methode;
    int donnees = (hH ? 1 : 0) + (hO ? 1 : 0) + (hA ? 1 : 0) + (hAng ? 1 : 0);
    if (donnees < 2) { err = "au moins 2 éléments parmi hypotenuse/oppose/adjacente/angle_deg requis"; return false; }
    if ((hH && H <= 0) || (hO && O <= 0) || (hA && A <= 0)) { err = "les côtés doivent être > 0"; return false; }
    if (hAng && (an <= 0 || an >= 90)) { err = "angle_deg doit être dans ]0, 90["; return false; }
    if (hO && hA) {
        H = std::sqrt(O * O + A * A); an = rad2deg(std::atan2(O, A));
        methode = "pythagore + arctangente (opposé & adjacent)";
    } else if (hH && hO) {
        if (O > H) { err = "oppose > hypotenuse : triangle impossible"; return false; }
        A = std::sqrt(H * H - O * O); an = rad2deg(std::asin(O / H));
        methode = "pythagore + arcsinus (hypoténuse & opposé)";
    } else if (hH && hA) {
        if (A > H) { err = "adjacente > hypotenuse : triangle impossible"; return false; }
        O = std::sqrt(H * H - A * A); an = rad2deg(std::acos(A / H));
        methode = "pythagore + arccosinus (hypoténuse & adjacente)";
    } else if (hO && hAng) {
        A = O / std::tan(deg2rad(an)); H = O / std::sin(deg2rad(an));
        methode = "tangente & sinus (opposé & angle)";
    } else if (hA && hAng) {
        O = A * std::tan(deg2rad(an)); H = A / std::cos(deg2rad(an));
        methode = "tangente & cosinus (adjacente & angle)";
    } else {  // hH && hAng
        O = H * std::sin(deg2rad(an)); A = H * std::cos(deg2rad(an));
        methode = "sinus & cosinus (hypoténuse & angle)";
    }
    out.set("hypotenuse", JVal::nombre(H));
    out.set("oppose", JVal::nombre(O));
    out.set("adjacente", JVal::nombre(A));
    out.set("angle_deg", JVal::nombre(an));
    out.set("angle_complementaire_deg", JVal::nombre(90.0 - an));
    out.set("methode", JVal::texte(methode));
    return true;
}

// ---- canonique.cercle ----
static bool op_canonique_cercle(const JVal& args, JVal& out, std::string& err) {
    std::vector<std::pair<double, double>> pts;
    if (!lire_points_xy(args, "points", pts, 3, err)) return false;
    double cx, cy, r;
    std::string methode;
    if (pts.size() == 3) {
        auto& p = pts;
        double d = 2.0 * (p[0].first * (p[1].second - p[2].second) +
                          p[1].first * (p[2].second - p[0].second) +
                          p[2].first * (p[0].second - p[1].second));
        if (std::fabs(d) < 1e-12) { err = "points alignés : pas de cercle défini"; return false; }
        double ux = ((p[0].first * p[0].first + p[0].second * p[0].second) * (p[1].second - p[2].second) +
                     (p[1].first * p[1].first + p[1].second * p[1].second) * (p[2].second - p[0].second) +
                     (p[2].first * p[2].first + p[2].second * p[2].second) * (p[0].second - p[1].second)) / d;
        double uy = ((p[0].first * p[0].first + p[0].second * p[0].second) * (p[2].first - p[1].first) +
                     (p[1].first * p[1].first + p[1].second * p[1].second) * (p[0].first - p[2].first) +
                     (p[2].first * p[2].first + p[2].second * p[2].second) * (p[1].first - p[0].first)) / d;
        cx = ux; cy = uy;
        r = std::sqrt((p[0].first - cx) * (p[0].first - cx) + (p[0].second - cy) * (p[0].second - cy));
        methode = "circumcentre exact (3 points)";
    } else {
        // Cercle de Kåsa : moindres carrés algébriques linéaires (centre 2×2).
        double sx = 0, sy = 0, sxx = 0, syy = 0, sxy = 0, sxxx = 0, syyy = 0, n = static_cast<double>(pts.size());
        for (auto& p : pts) {
            sx += p.first; sy += p.second;
            sxx += p.first * p.first; syy += p.second * p.second; sxy += p.first * p.second;
            sxxx += p.first * p.first * p.first + p.first * p.second * p.second;
            syyy += p.second * p.second * p.second + p.first * p.second * p.second;
        }
        std::vector<std::vector<double>> A{{2 * sxx, 2 * sxy}, {2 * sxy, 2 * syy}};
        std::vector<double> b{sxxx, syyy}, x;
        if (!gauss_resoudre(A, b, x)) { err = "points dégénérés : système singulier"; return false; }
        cx = x[0]; cy = x[1];
        double res = 0;
        for (auto& p : pts) {
            double di = std::sqrt((p.first - cx) * (p.first - cx) + (p.second - cy) * (p.second - cy));
            res += di;
        }
        r = res / n;
        methode = "moindres carrés algébriques (Kåsa) sur " + std::to_string(pts.size()) + " points";
    }
    JVal c = JVal::tableau();
    c.arr.push_back(JVal::nombre(cx));
    c.arr.push_back(JVal::nombre(cy));
    out.set("centre", c);
    out.set("rayon", JVal::nombre(r));
    out.set("equation", JVal::texte("(x - " + fmt_fr(cx) + ")^2 + (y - " + fmt_fr(cy) +
                                    ")^2 = " + fmt_fr(r) + "^2"));
    out.set("perimetre", JVal::nombre(2 * PI * r));
    out.set("aire", JVal::nombre(PI * r * r));
    out.set("methode", JVal::texte(methode));
    return true;
}

// ---- canonique.ellipse ----
static bool op_canonique_ellipse(const JVal& args, JVal& out, std::string& err) {
    std::vector<std::pair<double, double>> pts;
    if (!lire_points_xy(args, "points", pts, 5, err)) return false;
    // Fit algébrique (contrainte F = -1) : Ax^2 + Bxy + Cy^2 + Dx + Ey - 1 = 0.
    // Équations normales 5×5 (moindres carrés) -> élimination de Gauss.
    double S[5][5] = {{0}}, Sv[5] = {0};
    for (auto& p : pts) {
        double ligne[5] = {p.first * p.first, p.first * p.second, p.second * p.second,
                           p.first, p.second};
        for (int i = 0; i < 5; ++i) {
            for (int j = 0; j < 5; ++j) S[i][j] += ligne[i] * ligne[j];
            // Équation conique F = -1 : Ax² + Bxy + Cy² + Dx + Ey - 1 = 0,
            // donc Ax² + ... + Ey = +1 (second membre +1).
            Sv[i] += ligne[i] * 1.0;
        }
    }
    std::vector<std::vector<double>> A(5, std::vector<double>(5));
    std::vector<double> b(5);
    for (int i = 0; i < 5; ++i) {
        for (int j = 0; j < 5; ++j) A[i][j] = S[i][j];
        b[i] = Sv[i];
    }
    std::vector<double> sol;
    if (!gauss_resoudre(A, b, sol)) { err = "système singulier : points non elliptiques"; return false; }
    double Aa = sol[0], Bb = sol[1], Cc = sol[2], Dd = sol[3], Ee = sol[4];
    double delta = Bb * Bb - 4 * Aa * Cc;
    if (delta >= -1e-12) { err = "la conique ajustée n'est pas une ellipse (discriminant >= 0)"; return false; }
    // Centre : 2A x + B y + D = 0 ; B x + 2C y + E = 0
    double det = 4 * Aa * Cc - Bb * Bb;
    if (std::fabs(det) < 1e-15) { err = "centre indéterminé (conique dégénérée)"; return false; }
    double x0 = (-2 * Cc * Dd + Bb * Ee) / det;
    double y0 = (-2 * Aa * Ee + Bb * Dd) / det;
    // Constante au centre : F' = -1 + (D x0 + E y0)/2
    double Fp = -1.0 + (Dd * x0 + Ee * y0) / 2.0;
    double l1, l2;
    // Matrice de la forme quadratique : [[A, B/2], [B/2, C]] (B/2 hors diagonale —
    // le B de l'équation conique compte double dans le terme croisé).
    eig2_sym(Aa, Bb / 2.0, Cc, l1, l2);
    double d1 = -Fp / l1, d2 = -Fp / l2;
    if (d1 <= 0 || d2 <= 0) { err = "ellipse non réelle (constantes de signes incompatibles)"; return false; }
    double a = std::sqrt(d1), b2 = std::sqrt(d2);
    // Normalisation : a >= b ; rotation = angle propre correspondant.
    double rot;
    if (a >= b2) {
        rot = 0.5 * std::atan2(Bb, Aa - Cc);  // axe propre de l1 (matrice [[A, B/2], [B/2, C]])
    } else {
        std::swap(a, b2);
        rot = 0.5 * std::atan2(Bb, Aa - Cc) + PI / 2.0;
    }
    double rot_deg = std::fmod(rad2deg(rot), 180.0);
    if (rot_deg < 0) rot_deg += 180.0;
    JVal c = JVal::tableau();
    c.arr.push_back(JVal::nombre(x0));
    c.arr.push_back(JVal::nombre(y0));
    out.set("centre", c);
    out.set("demi_axe_a", JVal::nombre(a));
    out.set("demi_axe_b", JVal::nombre(b2));
    out.set("rotation_deg", JVal::nombre(rot_deg));
    out.set("excentricite", JVal::nombre(std::sqrt(std::max(0.0, 1.0 - (b2 * b2) / (a * a)))));
    out.set("aire", JVal::nombre(PI * a * b2));
    double h = ((a - b2) * (a - b2)) / ((a + b2) * (a + b2));
    out.set("perimetre_ramanujan", JVal::nombre(PI * (a + b2) * (1.0 + 3.0 * h / (10.0 + std::sqrt(4.0 - 3.0 * h)))));
    out.set("ratio_b_sur_a", JVal::nombre(b2 / a));
    out.set("equation", JVal::texte(
        "((x-" + fmt_fr(x0) + ")·cos(" + fmt_fr(rot_deg) + "°)+(y-" + fmt_fr(y0) + ")·sin(" +
        fmt_fr(rot_deg) + "°))²/" + fmt_fr(a * a) + " + (…)²/" + fmt_fr(b2 * b2) + " = 1"));
    out.set("methode", JVal::texte("fit algébrique (contrainte F=-1) + valeurs propres 2×2"));
    return true;
}

// ---- analyse.derivee ----
static bool op_analyse_derivee(const JVal& args, JVal& out, std::string& err) {
    if (args.has("fonction")) {
        std::string f = args.get_str("fonction", "");
        double x = args.get_num("x", 0.0), h = args.get_num("h", 1e-5);
        bool degres = args.get_str("unites", "rad") == "deg";
        if (h <= 0) { err = "'h' doit être > 0"; return false; }
        double f1, f2;
        if (!eval_fonction(f, x + h, 0, false, f1) || !eval_fonction(f, x - h, 0, false, f2)) {
            err = "fonction '" + f + "' inconnue ou hors domaine";
            return false;
        }
        out.set("fonction", JVal::texte(f));
        out.set("x", JVal::nombre(x));
        out.set("h", JVal::nombre(h));
        out.set("unites", JVal::texte(degres ? "deg" : "rad"));
        if (degres)
            out.set("avertissement", JVal::texte(
                "dérivée calculée en radians (unité naturelle des fonctions) — convertir si x est en degrés"));
        out.set("derivee", JVal::nombre((f1 - f2) / (2 * h)));
        out.set("methode", JVal::texte("differences-centrees (erreur O(h²))"));
        return true;
    }
    std::vector<std::pair<double, double>> pts;
    if (!lire_points_xy(args, "points", pts, 2, err)) return false;
    if (!args.has("x0")) { err = "'x0' requis avec 'points'"; return false; }
    double x0 = args.get_num("x0", 0.0);
    std::sort(pts.begin(), pts.end());
    if (x0 < pts.front().first - 1e-12 || x0 > pts.back().first + 1e-12) {
        err = "x0 hors du domaine des points";
        return false;
    }
    double d;
    std::string m;
    if (pts.size() == 2) {
        d = (pts[1].second - pts[0].second) / (pts[1].first - pts[0].first);
        m = "pente (2 points)";
    } else {
        // 3 points encadrants -> polynôme de Lagrange de degré 2, dérivée en x0.
        size_t i = 0;
        while (i + 2 < pts.size() && pts[i + 1].first < x0) ++i;
        double x1 = pts[i].first, y1 = pts[i].second;
        double x2 = pts[i + 1].first, y2 = pts[i + 1].second;
        double x3 = pts[i + 2].first, y3 = pts[i + 2].second;
        auto li = [&](double xx) {
            return y1 * (xx - x2) * (xx - x3) / ((x1 - x2) * (x1 - x3)) +
                   y2 * (xx - x1) * (xx - x3) / ((x2 - x1) * (x2 - x3)) +
                   y3 * (xx - x1) * (xx - x2) / ((x3 - x1) * (x3 - x2));
        };
        double e = 1e-7 * std::max(1.0, std::fabs(x0));
        d = (li(x0 + e) - li(x0 - e)) / (2 * e);
        m = "lagrange 3 points (dérivée du polynôme de degré 2)";
    }
    out.set("x0", JVal::nombre(x0));
    out.set("derivee", JVal::nombre(d));
    out.set("methode", JVal::texte(m));
    return true;
}

// ---- analyse.primitive ----
static bool op_analyse_primitive(const JVal& args, JVal& out, std::string& err) {
    if (args.has("coefficients")) {
        const JVal* c = args.get("coefficients");
        if (!c || c->t != JVal::ARR || c->arr.empty()) {
            err = "'coefficients' : tableau [c0, c1, ...] (polynôme c0 + c1·x + ...) requis";
            return false;
        }
        JVal prim = JVal::tableau();
        prim.arr.push_back(JVal::nombre(0.0));  // constante d'intégration C = 0
        std::string expr;
        for (size_t i = 0; i < c->arr.size(); ++i) {
            if (c->arr[i].t != JVal::NUM) { err = "coefficients non numériques"; return false; }
            double ci = c->arr[i].num;
            prim.arr.push_back(JVal::nombre(ci / static_cast<double>(i + 1)));
            if (ci != 0.0) {
                if (!expr.empty()) expr += " + ";
                double v = ci / static_cast<double>(i + 1);
                if (i == 0) {
                    expr += fmt_fr(v);
                } else if (i == 1) {
                    expr += fmt_fr(v) + "·x";
                } else {
                    expr += fmt_fr(v) + "·x^" + std::to_string(i + 1);
                }
            }
        }
        if (expr.empty()) expr = "0";
        out.set("coefficients_primitive", prim);
        out.set("expression", JVal::texte(expr + " + C"));
        out.set("note", JVal::texte("constante d'intégration C = 0 (convention)"));
        return true;
    }
    if (args.has("fonction")) {
        std::string f = args.get_str("fonction", "");
        double a = args.get_num("a", 0.0), b = args.get_num("b", 0.0);
        double v1, v2;
        if (!eval_fonction(f, a, 0, false, v1) || !eval_fonction(f, b, 0, false, v2)) {
            err = "fonction '" + f + "' inconnue ou hors domaine";
            return false;
        }
        out.set("fonction", JVal::texte(f));
        out.set("a", JVal::nombre(a));
        out.set("b", JVal::nombre(b));
        out.set("primitive_definie", JVal::nombre(
            gauss5_compose([&](double t) { double v; eval_fonction(f, t, 0, false, v); return v; },
                           a, b, 1000)));
        out.set("methode", JVal::texte("gauss-legendre 5 points composé (1000 intervalles)"));
        return true;
    }
    err = "'coefficients' (primitive formelle) ou 'fonction'+'a'+'b' (primitive définie) requis";
    return false;
}

// ---- analyse.integrale ----
static bool op_analyse_integrale(const JVal& args, JVal& out, std::string& err) {
    if (args.has("fonction")) {
        std::string f = args.get_str("fonction", "");
        double a = args.get_num("a", 0.0), b = args.get_num("b", 0.0);
        int n = static_cast<int>(args.get_num("n", 1000));
        if (n < 1 || n > 1000000) { err = "'n' doit être dans [1, 1000000]"; return false; }
        double echant;
        if (!eval_fonction(f, a, 0, false, echant)) {
            err = "fonction '" + f + "' inconnue ou hors domaine en a";
            return false;
        }
        out.set("fonction", JVal::texte(f));
        out.set("a", JVal::nombre(a));
        out.set("b", JVal::nombre(b));
        out.set("integrale", JVal::nombre(gauss5_compose(
            [&](double t) { double v; eval_fonction(f, t, 0, false, v); return v; }, a, b, n)));
        out.set("methode", JVal::texte("gauss-legendre 5 points composé"));
        out.set("nb_intervalles", JVal::nombre(n));
        out.set("tolerance", JVal::texte("1e-6 (Gauss 5 points — enseignement d'origine)"));
        return true;
    }
    std::vector<std::pair<double, double>> pts;
    if (!lire_points_xy(args, "points", pts, 2, err)) return false;
    std::sort(pts.begin(), pts.end());
    double s = 0.0;
    std::string m;
    for (size_t i = 0; i + 1 < pts.size(); ++i) {
        double dx = pts[i + 1].first - pts[i].first;
        if (dx < 0) { err = "abscisses non croissantes après tri"; return false; }
        if ((pts.size() - 1) % 2 == 1 && i + 2 == pts.size()) {
            s += dx * (pts[i + 1].second + pts[i].second) / 2.0;  // dernier trapèze
            m = "simpson composite (dernier intervalle en trapèze — nb de points pair)";
        } else if (i % 2 == 0 && i + 2 < pts.size()) {
            double h = dx;
            s += h / 3.0 * (pts[i].second + 4 * pts[i + 1].second + pts[i + 2].second);
            if (m.empty()) m = "simpson composite";
        } else if (i + 2 == pts.size() && i % 2 == 1) {
            // couvert par le trapèze ci-dessus ou simpson précédent
        } else if (pts.size() == 2) {
            s += dx * (pts[i + 1].second + pts[i].second) / 2.0;
            m = "trapeze (2 points)";
        }
    }
    out.set("integrale", JVal::nombre(s));
    out.set("methode", JVal::texte(m.empty() ? "simpson composite" : m));
    out.set("nb_points", JVal::nombre(static_cast<double>(pts.size())));
    return true;
}

// ---- fourier.serie ----
static bool op_fourier_serie(const JVal& args, JVal& out, std::string& err) {
    std::string f = args.get_str("fonction", "");
    double T = args.get_num("periode", 0.0);
    int H = static_cast<int>(args.get_num("harmoniques", 5));
    double centre = args.get_num("centre", 0.0);
    if (f.empty()) { err = "'fonction' requis"; return false; }
    if (T <= 0) { err = "'periode' doit être > 0"; return false; }
    if (H < 1 || H > 64) { err = "'harmoniques' doit être dans [1, 64]"; return false; }
    double echant;
    if (!eval_fonction(f, centre, 0, false, echant)) {
        err = "fonction '" + f + "' inconnue ou hors domaine";
        return false;
    }
    auto fn = [&](double t) { double v; eval_fonction(f, t, 0, false, v); return v; };
    double w = 2 * PI / T;
    double a0 = 2.0 / T * gauss5_compose(fn, centre - T / 2, centre + T / 2, 400);
    JVal an = JVal::tableau(), bn = JVal::tableau();
    for (int k = 1; k <= H; ++k) {
        double cn = 2.0 / T * gauss5_compose([&](double t) { return fn(t) * std::cos(k * w * t); },
                                             centre - T / 2, centre + T / 2, 400);
        double sn = 2.0 / T * gauss5_compose([&](double t) { return fn(t) * std::sin(k * w * t); },
                                             centre - T / 2, centre + T / 2, 400);
        an.arr.push_back(JVal::nombre(cn));
        bn.arr.push_back(JVal::nombre(sn));
    }
    out.set("fonction", JVal::texte(f));
    out.set("periode", JVal::nombre(T));
    out.set("harmoniques", JVal::nombre(H));
    out.set("a0", JVal::nombre(a0));
    out.set("an", an);
    out.set("bn", bn);
    out.set("convention", JVal::texte("f(t) ≈ a0/2 + Σ [an·cos(2πkt/T) + bn·sin(2πkt/T)]"));
    out.set("methode", JVal::texte("coefficients par intégration gauss-legendre 5 points composée"));
    return true;
}

// ---- fourier.eval ----
static bool op_fourier_eval(const JVal& args, JVal& out, std::string& err) {
    if (!args.has("a0") || !args.has("an") || !args.has("bn")) {
        err = "'a0', 'an', 'bn' requis (sortie de fourier.serie)";
        return false;
    }
    double T = args.get_num("periode", 2 * PI);
    if (T <= 0) { err = "'periode' doit être > 0"; return false; }
    double x = args.get_num("x", 0.0);
    double a0 = args.get_num("a0", 0.0);
    const JVal* an = args.get("an");
    const JVal* bn = args.get("bn");
    if (!an || !bn || an->t != JVal::ARR || bn->t != JVal::ARR || an->arr.size() != bn->arr.size()) {
        err = "'an' et 'bn' doivent être des tableaux de même longueur";
        return false;
    }
    double w = 2 * PI / T, s = a0 / 2.0;
    for (size_t k = 0; k < an->arr.size(); ++k) {
        double kk = static_cast<double>(k + 1);
        s += an->arr[k].num * std::cos(kk * w * x) + bn->arr[k].num * std::sin(kk * w * x);
    }
    out.set("valeur", JVal::nombre(s));
    out.set("x", JVal::nombre(x));
    out.set("periode", JVal::nombre(T));
    out.set("harmoniques_utilises", JVal::nombre(static_cast<double>(an->arr.size())));
    return true;
}

// ---- euler.formule ----
static bool op_euler_formule(const JVal& args, JVal& out, std::string& err) {
    double theta;
    if (args.has("theta_deg")) {
        theta = deg2rad(args.get_num("theta_deg", 0.0));
        out.set("theta_deg", JVal::nombre(args.get_num("theta_deg", 0.0)));
    } else if (args.has("theta")) {
        theta = args.get_num("theta", 0.0);
        out.set("theta_deg", JVal::nombre(rad2deg(theta)));
    } else {
        err = "'theta' (radians) ou 'theta_deg' (degrés) requis";
        return false;
    }
    double arg = std::fmod(theta + PI, 2 * PI);
    if (arg < 0) arg += 2 * PI;
    arg -= PI;
    out.set("theta", JVal::nombre(theta));
    out.set("re", JVal::nombre(std::cos(theta)));
    out.set("im", JVal::nombre(std::sin(theta)));
    out.set("module", JVal::nombre(1.0));
    out.set("argument", JVal::nombre(arg));
    out.set("forme", JVal::texte("e^(i·θ) = cos θ + i·sin θ = " + fmt_fr(std::cos(theta)) +
                                 (std::sin(theta) < 0 ? " - " : " + ") +
                                 fmt_fr(std::fabs(std::sin(theta))) + "·i"));
    return true;
}

// ---- euler.rotation ----
static bool op_euler_rotation(const JVal& args, JVal& out, std::string& err) {
    const JVal* ang = args.get("angles_deg");
    if (!ang || ang->t != JVal::ARR || ang->arr.size() != 3) {
        err = "'angles_deg' : [alpha, beta, gamma] requis (degrés)";
        return false;
    }
    for (auto& a : ang->arr)
        if (a.t != JVal::NUM) { err = "angles non numériques"; return false; }
    std::string ordre = args.get_str("ordre", "ZXZ");
    double al = deg2rad(ang->arr[0].num), be = deg2rad(ang->arr[1].num),
           ga = deg2rad(ang->arr[2].num);
    Mat3 R;
    if (ordre == "ZXZ") R = rotation_z(al).multiplie(rotation_x(be)).multiplie(rotation_z(ga));
    else if (ordre == "ZYZ") R = rotation_z(al).multiplie(rotation_y(be)).multiplie(rotation_z(ga));
    else if (ordre == "XYZ") R = rotation_x(al).multiplie(rotation_y(be)).multiplie(rotation_z(ga));
    else if (ordre == "ZYX") R = rotation_z(al).multiplie(rotation_y(be)).multiplie(rotation_x(ga));
    else { err = "ordre inconnu (ZXZ, ZYZ, XYZ ou ZYX)"; return false; }
    double q[4];
    quaternion_depuis_mat3(R, q);
    JVal M = JVal::tableau();
    for (int i = 0; i < 3; ++i) {
        JVal ligne = JVal::tableau();
        for (int j = 0; j < 3; ++j) ligne.arr.push_back(JVal::nombre(R.m[i][j]));
        M.arr.push_back(ligne);
    }
    JVal Q = JVal::tableau();
    for (double v : q) Q.arr.push_back(JVal::nombre(v));
    out.set("angles_deg", *ang);
    out.set("ordre", JVal::texte(ordre));
    out.set("matrice", M);
    out.set("quaternion", Q);  // [w, x, y, z]
    const JVal* p = args.get("point");
    if (p && p->t == JVal::ARR && p->arr.size() == 3) {
        Vec3 v(p->arr[0].num, p->arr[1].num, p->arr[2].num);
        Vec3 r = R.applique(v);
        JVal P = JVal::tableau();
        P.arr.push_back(JVal::nombre(r.x));
        P.arr.push_back(JVal::nombre(r.y));
        P.arr.push_back(JVal::nombre(r.z));
        out.set("point_tourne", P);
    }
    return true;
}

// ---- euler.projection ----
static bool op_euler_projection(const JVal& args, JVal& out, std::string& err) {
    double az = args.get_num("azimut_deg", 45.0);
    double el = args.get_num("elevation_deg", ISO_ELEV_DEG);
    if (el <= 0 || el >= 90) { err = "'elevation_deg' doit être dans ]0, 90["; return false; }
    Iso iso(az, el);
    JVal M = JVal::tableau();
    JVal l1 = JVal::tableau();
    l1.arr.push_back(JVal::nombre(iso.right.x));
    l1.arr.push_back(JVal::nombre(iso.right.y));
    l1.arr.push_back(JVal::nombre(iso.right.z));
    JVal l2 = JVal::tableau();
    l2.arr.push_back(JVal::nombre(iso.up.x));
    l2.arr.push_back(JVal::nombre(iso.up.y));
    l2.arr.push_back(JVal::nombre(iso.up.z));
    M.arr.push_back(l1);
    M.arr.push_back(l2);
    const JVal* p = args.get("point");
    if (p && p->t == JVal::ARR && p->arr.size() == 3) {
        Vec3 v(p->arr[0].num, p->arr[1].num, p->arr[2].num);
        JVal P2 = JVal::tableau();
        P2.arr.push_back(JVal::nombre(iso.u(v)));
        P2.arr.push_back(JVal::nombre(iso.v(v)));
        out.set("point_2d", P2);
    }
    double ratio_vs = iso.ratio_cap();
    double theo = std::sin(deg2rad(el));
    out.set("azimut_deg", JVal::nombre(az));
    out.set("elevation_deg", JVal::nombre(el));
    out.set("matrice_uv", M);
    out.set("ratio_cap_valeurs_singulieres", JVal::nombre(ratio_vs));
    out.set("ratio_theorique_sin_elevation", JVal::nombre(theo));
    out.set("concordance", JVal::boo(std::fabs(ratio_vs - theo) < 1e-9));
    out.set("convention", JVal::texte("u = P·right, v = P·up (+z monde vers le haut de l'écran) — isométrie CAO"));
    out.set("note", JVal::texte("ratio du petit axe d'un cercle horizontal par VALEURS SINGULIÈRES de la sous-application (le ratio bbox d'une ellipse inclinée est faux — enseignement d'origine)"));
    return true;
}

// ---- euler.caracteristique ----
static bool op_euler_caracteristique(const JVal& args, JVal& out, std::string& err) {
    const JVal* Mj = args.get("matrice");
    if (!Mj || Mj->t != JVal::ARR || Mj->arr.size() != 3) {
        err = "'matrice' : 3×3 requise";
        return false;
    }
    Mat3 R;
    for (int i = 0; i < 3; ++i) {
        if (Mj->arr[i].t != JVal::ARR || Mj->arr[i].arr.size() != 3) {
            err = "'matrice' : 3×3 requise";
            return false;
        }
        for (int j = 0; j < 3; ++j) {
            if (Mj->arr[i].arr[j].t != JVal::NUM) { err = "matrice non numérique"; return false; }
            R.m[i][j] = Mj->arr[i].arr[j].num;
        }
    }
    double det = R.determinant();
    double tr = R.trace();
    if (std::fabs(det - 1.0) > 1e-9)
        out.set("avertissement", JVal::texte("det = " + fmt_fr(det, 6) + " ≠ 1 : la matrice n'est pas une rotation pure"));
    double cosT = (tr - 1.0) / 2.0;
    if (cosT > 1.0) cosT = 1.0;
    if (cosT < -1.0) cosT = -1.0;
    double theta = std::acos(cosT);
    double sinT = std::sin(theta);
    Vec3 axe;
    std::string cas = "general";
    double q[4];
    if (sinT < 1e-8) {
        if (cosT > 0.0) {
            cas = "angle-nul (axe indéterminé, convention z)";
            axe = Vec3(0, 0, 1);
        } else {
            cas = "angle-pi (axe depuis la colonne dominante de (R+I)/2)";
            Mat3 P;
            for (int i = 0; i < 3; ++i)
                for (int j = 0; j < 3; ++j)
                    P.m[i][j] = (R.m[i][j] + (i == j ? 1.0 : 0.0)) / 2.0;
            int k = 0;
            if (P.m[1][1] > P.m[k][k]) k = 1;
            if (P.m[2][2] > P.m[k][k]) k = 2;
            axe = P.colonne(k).normalise();
        }
        quaternion_depuis_mat3(R, q);
    } else {
        axe = Vec3(R.m[2][1] - R.m[1][2], R.m[0][2] - R.m[2][0], R.m[1][0] - R.m[0][1])
                  .normalise();
        quaternion_depuis_mat3(R, q);
    }
    JVal A = JVal::tableau();
    A.arr.push_back(JVal::nombre(axe.x));
    A.arr.push_back(JVal::nombre(axe.y));
    A.arr.push_back(JVal::nombre(axe.z));
    JVal Q = JVal::tableau();
    for (double v : q) Q.arr.push_back(JVal::nombre(v));
    out.set("angle_deg", JVal::nombre(rad2deg(theta)));
    out.set("axe", A);
    out.set("quaternion", Q);
    out.set("trace", JVal::nombre(tr));
    out.set("determinant", JVal::nombre(det));
    out.set("cas", JVal::texte(cas));
    return true;
}

// ============================ Géométrie des pièces ============================

struct Segment {
    double x0 = 0, x1 = 0, d0 = 0, d1 = 0;  // x le long de l'axe ; diamètres aux extrémités
    int facettes = 0;                         // 0 = rond ; 6 = hexagone (d = entre-pointes)
    std::string note;
    double r0_eff = 0, r1_eff = 0;            // rayons EFFECTIFS (moyen sommets/apothème si facettes)
};

static bool lire_segments(const JVal& args, std::vector<Segment>& segs,
                          std::vector<double>& bores, std::string& err) {
    const JVal* a = args.get("segments");
    if (!a || a->t != JVal::ARR || a->arr.empty()) {
        err = "'segments' : tableau non vide requis [{x0, x1, d, d2?, facettes?, note?}]";
        return false;
    }
    for (const JVal& s : a->arr) {
        if (s.t != JVal::OBJ || !s.has("x0") || !s.has("x1") || !s.has("d")) {
            err = "chaque segment exige x0, x1, d (numériques)";
            return false;
        }
        Segment g;
        g.x0 = s.get_num("x0", 0);
        g.x1 = s.get_num("x1", 0);
        g.d0 = s.get_num("d", 0);
        g.d1 = s.get_num("d2", g.d0);
        if (s.has("d2")) g.d1 = s.get_num("d2", g.d0);
        g.facettes = static_cast<int>(s.get_num("facettes", 0));
        g.note = s.get_str("note", "");
        if (!(g.x0 < g.x1)) { err = "segment avec x0 >= x1"; return false; }
        if (g.d0 <= 0 || g.d1 <= 0) { err = "diamètres <= 0"; return false; }
        if (g.facettes != 0 && g.facettes < 3) { err = "facettes doit être >= 3 (ou 0 = rond)"; return false; }
        if (g.facettes > 0) {
            double apoth = std::cos(PI / g.facettes);
            g.r0_eff = (g.d0 / 4.0) * (1.0 + apoth);
            g.r1_eff = (g.d1 / 4.0) * (1.0 + apoth);
        } else {
            g.r0_eff = g.d0 / 2.0;
            g.r1_eff = g.d1 / 2.0;
        }
        segs.push_back(g);
    }
    std::sort(segs.begin(), segs.end(),
              [](const Segment& a, const Segment& b) { return a.x0 < b.x0; });
    for (size_t i = 0; i + 1 < segs.size(); ++i)
        if (segs[i].x1 > segs[i + 1].x0 + 1e-9) {
            err = "segments qui se chevauchent (x1 = " + fmt_fr(segs[i].x1) +
                  " > x0 suivant = " + fmt_fr(segs[i + 1].x0) + ")";
            return false;
        }
    const JVal* bb = args.get("bores");
    if (bb && bb->t == JVal::ARR)
        for (const JVal& b : bb->arr) {
            if (b.t != JVal::NUM || b.num <= 0) { err = "bores : diamètres > 0 requis"; return false; }
            bores.push_back(b.num);
        }
    return true;
}

static std::vector<std::string> cotes_du_profil(const std::vector<Segment>& segs,
                                                const std::vector<double>& bores) {
    std::vector<std::string> cotes;
    for (const auto& s : segs) {
        double L = s.x1 - s.x0;
        std::string prefixe = s.note.empty() ? "" : s.note + " : ";
        if (s.facettes == 6) {
            cotes.push_back(prefixe + "hex " + fmt_fr(s.d0) + " entre-pointes × " + fmt_fr(L) + " mm");
        } else if (s.facettes > 0) {
            cotes.push_back(prefixe + "prisme " + std::to_string(s.facettes) + " facettes Ø " +
                            fmt_fr(s.d0) + " × " + fmt_fr(L) + " mm");
        } else if (std::fabs(s.d0 - s.d1) > 1e-12) {
            cotes.push_back(prefixe + "Ø " + fmt_fr(s.d0) + " → Ø " + fmt_fr(s.d1) + " × " +
                            fmt_fr(L) + " mm (cône)");
        } else {
            cotes.push_back(prefixe + "Ø " + fmt_fr(s.d0) + " × " + fmt_fr(L) + " mm");
        }
    }
    for (double b : bores) cotes.push_back("bore Ø " + fmt_fr(b) + " mm");
    double L = segs.back().x1 - segs.front().x0;
    double dmax = 0;
    for (const auto& s : segs) dmax = std::max(dmax, std::max(s.d0, s.d1));
    cotes.push_back("longueur totale " + fmt_fr(L) + " mm");
    cotes.push_back("Ø max " + fmt_fr(dmax) + " mm");
    return cotes;
}

// ---- piece.profil_2d ----
static bool op_piece_profil_2d(const JVal& args, JVal& out, std::string& err) {
    std::vector<Segment> segs;
    std::vector<double> bores;
    if (!lire_segments(args, segs, bores, err)) return false;
    // Intégrales exactes de la demi-section (r(x) linéaire par morceaux) :
    //   A = ∫r dx ; S = ∫r²/2 dx ; Ix_axe = ∫r³/3 dx ; Iy0 = ∫x²·r dx ; Mx = ∫x·r dx
    double A = 0, S = 0, Ix_axe = 0, Iy0 = 0, Mx = 0;
    for (const auto& s : segs) {
        double L = s.x1 - s.x0, r0 = s.r0_eff, r1 = s.r1_eff;
        A += (r0 + r1) / 2.0 * L;
        S += (r0 * r0 + r0 * r1 + r1 * r1) / 6.0 * L;
        Ix_axe += (r0 * r0 * r0 + r0 * r0 * r1 + r0 * r1 * r1 + r1 * r1 * r1) / 12.0 * L;
        // ∫x²·r dx et ∫x·r dx : formules fermées sur x = x0 + t·L, r = r0 + t·(r1-r0)/L
        double dr = (r1 - r0) / L;
        for (int terme = 0; terme < 2; ++terme) {
            // terme 0 : part constante r0 ; terme 1 : part linéaire dr·(x - x0)
            double c = (terme == 0) ? r0 : dr;
            if (terme == 0) {
                Iy0 += c * (std::pow(s.x1, 3) - std::pow(s.x0, 3)) / 3.0;
                Mx += c * (s.x1 * s.x1 - s.x0 * s.x0) / 2.0;
            } else {
                Iy0 += c * (std::pow(s.x1, 4) - std::pow(s.x0, 4)) / 4.0 -
                       c * s.x0 * (std::pow(s.x1, 3) - std::pow(s.x0, 3)) / 3.0;
                Mx += c * (std::pow(s.x1, 3) - std::pow(s.x0, 3)) / 3.0 -
                      c * s.x0 * (s.x1 * s.x1 - s.x0 * s.x0) / 2.0;
            }
        }
    }
    double y_bar = S / A, x_bar = Mx / A;
    double Ix_c = Ix_axe - y_bar * y_bar * A;   // demi-section, axes au centroïde
    double Iy_c = Iy0 - x_bar * x_bar * A;
    double volume = 2 * PI * y_bar * A;          // théorème de Guldin-Pappus
    // Contour FERMÉ de la demi-section — ARÊTES LOCALES : chaque jonction est
    // résolue par SES deux segments adjacents (enseignement d'origine : jamais
    // de résolution globale des hauteurs de bord).
    JVal contour = JVal::tableau();
    auto push = [&contour](double x, double y) {
        JVal p = JVal::tableau();
        p.arr.push_back(JVal::nombre(x));
        p.arr.push_back(JVal::nombre(y));
        contour.arr.push_back(p);
    };
    push(segs.front().x0, 0.0);
    for (const auto& s : segs) {
        push(s.x0, s.r0_eff);  // marche verticale locale (jonction gauche)
        push(s.x1, s.r1_eff);  // flanc (cylindre ou tronc de cône)
    }
    push(segs.back().x1, 0.0);
    // avertissements : trous entre segments (décroissance vers l'axe documentée)
    JVal avert = JVal::tableau();
    for (size_t i = 0; i + 1 < segs.size(); ++i)
        if (segs[i].x1 < segs[i + 1].x0 - 1e-9)
            avert.arr.push_back(JVal::texte(
                "segment manquant entre x = " + fmt_fr(segs[i].x1) + " et x = " +
                fmt_fr(segs[i + 1].x0) + " — traité comme décroissance vers l'axe"));
    for (const auto& s : segs)
        if (s.facettes > 0)
            avert.arr.push_back(JVal::texte(
                "segment " + (s.note.empty() ? std::to_string(static_cast<int>(&s - segs.data())) : s.note) +
                " : profil équivalent au rayon moyen (sommets + apothème)/2"));
    JVal demi = JVal::objet();
    demi.set("aire_mm2", JVal::nombre(A));
    demi.set("x_centroide", JVal::nombre(x_bar));
    demi.set("y_centroide", JVal::nombre(y_bar));
    JVal section = JVal::objet();
    section.set("aire_mm2", JVal::nombre(2 * A));
    section.set("ix_autour_axe_mm4", JVal::nombre(2 * Ix_axe));
    section.set("iy_centroide_mm4", JVal::nombre(2 * Iy_c));
    section.set("ix_demi_centroide_mm4", JVal::nombre(Ix_c));
    JVal solide = JVal::objet();
    solide.set("volume_guldin_mm3", JVal::nombre(volume));
    solide.set("methode", JVal::texte("théorème de Guldin-Pappus : V = 2π·ȳ·A_demi"));
    JVal mesures = JVal::objet();
    mesures.set("longueur_totale_mm", JVal::nombre(segs.back().x1 - segs.front().x0));
    double dmax = 0;
    for (const auto& s : segs) dmax = std::max(dmax, std::max(s.d0, s.d1));
    mesures.set("diametre_max_mm", JVal::nombre(dmax));
    JVal cotes = JVal::tableau();
    for (const std::string& c : cotes_du_profil(segs, bores)) cotes.arr.push_back(JVal::texte(c));
    JVal bj = JVal::tableau();
    for (double b : bores) bj.arr.push_back(JVal::nombre(b));
    out.set("segments_lus", JVal::nombre(static_cast<double>(segs.size())));
    out.set("bores", bj);
    out.set("mesures", mesures);
    out.set("aires", demi);
    out.set("section_axiale", section);
    out.set("solide", solide);
    out.set("contour_demi_section", contour);
    out.set("cotes", cotes);
    if (!avert.arr.empty()) out.set("avertissements", avert);
    out.set("note", JVal::texte("aires/inerties sur le profil EXTÉRIEUR ; bores rapportés en cotes (cotation) ; contour = demi-section fermée prête au rendu"));
    return true;
}

// ---- piece.modele_iso ----

struct ItemRendu {
    std::string type;    // "face" | "trait"
    std::string role;    // flanc | dessus | dessous | cap | bore
    std::string couleur;
    std::vector<std::pair<double, double>> points;  // 2D projeté
    double zc = 0;                                    // profondeur (grand = proche)
};

static void emettre_face(std::vector<ItemRendu>& items, const std::vector<Vec3>& sommets3,
                         const Vec3& normale, const Iso& iso, const std::string& role,
                         const std::string& couleur) {
    // Face visible seulement si sa normale tournée pointe vers la caméra
    // (généralisation de l'enseignement « caps visibles n′z > 0 »).
    if (normale.dot(iso.dir) <= 0) return;
    ItemRendu it;
    it.type = "face";
    it.role = role;
    it.couleur = couleur;
    double zsum = 0;
    for (const Vec3& p : sommets3) {
        it.points.emplace_back(iso.u(p), iso.v(p));
        zsum += iso.profondeur(p);
    }
    it.zc = zsum / static_cast<double>(sommets3.size());
    items.push_back(it);
}

static void emettre_trait(std::vector<ItemRendu>& items, const Vec3& a, const Vec3& b,
                          const Iso& iso, const std::string& role) {
    ItemRendu it;
    it.type = "trait";
    it.role = role;
    it.couleur = "#4b4b51";
    it.points.emplace_back(iso.u(a), iso.v(a));
    it.points.emplace_back(iso.u(b), iso.v(b));
    it.zc = (iso.profondeur(a) + iso.profondeur(b)) / 2.0;
    items.push_back(it);
}

static std::string couleur_flanc(const Vec3& n, const Iso& iso) {
    if (n.z > 0.7) return "#d8d8f8";   // dessus lavande (DNA)
    if (n.z < -0.7) return "#a0a0a8";  // dessous (DNA)
    // Deux tons de gris déterministes selon l'orientation écran (DNA)
    return (n.dot(iso.right) >= 0.0) ? "#b8b8c0" : "#a8a8b0";
}

static bool op_piece_modele_iso(const JVal& args, JVal& out, std::string& err) {
    std::string type = args.get_str("type", "");
    double az = args.get_num("azimut_deg", 45.0);
    double el = args.get_num("elevation_deg", ISO_ELEV_DEG);
    int N = static_cast<int>(args.get_num("echantillons", 48));
    if (el <= 0 || el >= 90) { err = "'elevation_deg' doit être dans ]0, 90["; return false; }
    if (N < 8 || N > 256) { err = "'echantillons' doit être dans [8, 256]"; return false; }
    Iso iso(az, el);
    std::vector<ItemRendu> items;
    JVal cotes = JVal::tableau();

    if (type == "boite") {
        double lx = args.get_num("lx", 0), ly = args.get_num("ly", 0), lz = args.get_num("lz", 0);
        if (lx <= 0 || ly <= 0 || lz <= 0) { err = "lx, ly, lz > 0 requis"; return false; }
        Vec3 v[8] = {{0, 0, 0}, {lx, 0, 0}, {lx, ly, 0}, {0, ly, 0},
                     {0, 0, lz}, {lx, 0, lz}, {lx, ly, lz}, {0, ly, lz}};
        int faces[6][4] = {{4, 5, 6, 7}, {1, 0, 3, 2}, {0, 1, 5, 4},
                           {3, 7, 6, 2}, {0, 4, 7, 3}, {1, 2, 6, 5}};
        Vec3 norm[6] = {{0, 0, 1}, {0, 0, -1}, {0, -1, 0}, {0, 1, 0}, {-1, 0, 0}, {1, 0, 0}};
        const char* roles[6] = {"dessus", "dessous", "flanc", "flanc", "flanc", "flanc"};
        for (int f = 0; f < 6; ++f) {
            std::vector<Vec3> poly{v[faces[f][0]], v[faces[f][1]], v[faces[f][2]], v[faces[f][3]]};
            emettre_face(items, poly, norm[f], iso, roles[f], couleur_flanc(norm[f], iso));
        }
        cotes.arr.push_back(JVal::texte("boîte " + fmt_fr(lx) + " × " + fmt_fr(ly) + " × " +
                                        fmt_fr(lz) + " mm"));
    } else if (type == "cylindre") {
        double d = args.get_num("d", 0), h = args.get_num("h", 0);
        if (d <= 0 || h <= 0) { err = "d, h > 0 requis"; return false; }
        double r = d / 2.0;
        auto pt = [&](int i, double zz) {
            double t = 2 * PI * i / N;
            return Vec3(r * std::cos(t), r * std::sin(t), zz);
        };
        for (int i = 0; i < N; ++i) {
            Vec3 a = pt(i, 0), b = pt(i + 1, 0), c = pt(i + 1, h), e = pt(i, h);
            Vec3 milieu((a.x + c.x) / 2, (a.y + c.y) / 2, 0);
            Vec3 n = Vec3(milieu.x, milieu.y, 0).normalise();
            emettre_face(items, {a, b, c, e}, n, iso, "flanc", couleur_flanc(n, iso));
        }
        std::vector<Vec3> cap_h, cap_b;
        for (int i = 0; i < N; ++i) cap_h.push_back(pt(i, h));
        for (int i = 0; i < N; ++i) cap_b.push_back(pt(N - i, 0));
        emettre_face(items, cap_h, Vec3(0, 0, 1), iso, "dessus", "#d8d8f8");
        emettre_face(items, cap_b, Vec3(0, 0, -1), iso, "dessous", "#a0a0a8");
        // arcs de silhouette : arêtes des faces rendues (moitié externe incluse
        // par construction — seuls les secteurs visibles sont émis)
        for (int i = 0; i < N; ++i) {
            Vec3 a = pt(i, 0), b = pt(i + 1, 0), c = pt(i + 1, h), e = pt(i, h);
            Vec3 milieu((a.x + c.x) / 2, (a.y + c.y) / 2, 0);
            Vec3 n = Vec3(milieu.x, milieu.y, 0).normalise();
            if (n.dot(iso.dir) > 0) {
                emettre_trait(items, a, e, iso, "arete");
                emettre_trait(items, b, c, iso, "arete");
            }
        }
        cotes.arr.push_back(JVal::texte("Ø " + fmt_fr(d) + " × " + fmt_fr(h) + " mm"));
    } else if (type == "revolution") {
        std::vector<Segment> segs;
        std::vector<double> bores;
        if (!lire_segments(args, segs, bores, err)) return false;
        // Axe = X (cohérent avec piece.profil_2d), r dans le plan YZ.
        // Chaque segment = tronc de cône/cylindre échantillonné ; facettes = prisme.
        for (const auto& s : segs) {
            int NS = s.facettes > 0 ? s.facettes : N;
            double rap0 = s.facettes > 0 ? (s.d0 / 2.0) : s.r0_eff;
            double rap1 = s.facettes > 0 ? (s.d1 / 2.0) : s.r1_eff;
            // polygone régulier : rayon au sommet (pour facettes, d = entre-pointes
            // est le rayon au sommet = r_circumscribed)
            auto pt = [&](int i, double x, double rc) {
                double t = 2 * PI * i / NS;
                return Vec3(x, rc * std::cos(t), rc * std::sin(t));
            };
            // flancs (quadrilatères entre anneaux x0 et x1)
            for (int i = 0; i < NS; ++i) {
                Vec3 a = pt(i, s.x0, rap0), b = pt(i + 1, s.x0, rap0);
                Vec3 c = pt(i + 1, s.x1, rap1), e = pt(i, s.x1, rap1);
                Vec3 mid0 = pt(i, (s.x0 + s.x1) / 2, (rap0 + rap1) / 2);
                Vec3 radial(0, mid0.y, mid0.z);
                if (radial.norme() < 1e-12) continue;
                Vec3 n = radial.normalise();
                emettre_face(items, {a, b, c, e}, n, iso, "flanc", couleur_flanc(n, iso));
                if (n.dot(iso.dir) > 0) {
                    emettre_trait(items, a, e, iso, "arete");
                    emettre_trait(items, b, c, iso, "arete");
                }
            }
            // cap gauche (x0) : visible si -X pointe vers la caméra
            {
                std::vector<Vec3> cap;
                for (int i = 0; i < NS; ++i) cap.push_back(pt(NS - i, s.x0, rap0));
                emettre_face(items, cap, Vec3(-1, 0, 0), iso, "cap", "#b8b8c0");
                // traits du contour du cap visible (arc externe inclus par visibilité)
                if (Vec3(-1, 0, 0).dot(iso.dir) > 0) {
                    for (int i = 0; i < NS; ++i) {
                        Vec3 a = pt(i, s.x0, rap0), b = pt(i + 1, s.x0, rap0);
                        Vec3 mid((a.y + b.y) / 2, (a.z + b.z) / 2, 0);
                        Vec3 n(0, mid.y, mid.z);
                        if (n.normalise().dot(iso.dir) > 0.3)
                            emettre_trait(items, a, b, iso, "arete");
                    }
                }
            }
            // cap droit (x1)
            {
                std::vector<Vec3> cap;
                for (int i = 0; i < NS; ++i) cap.push_back(pt(i, s.x1, rap1));
                emettre_face(items, cap, Vec3(1, 0, 0), iso, "cap", "#b8b8c0");
                if (Vec3(1, 0, 0).dot(iso.dir) > 0) {
                    for (int i = 0; i < NS; ++i) {
                        Vec3 a = pt(i, s.x1, rap1), b = pt(i + 1, s.x1, rap1);
                        Vec3 mid((a.y + b.y) / 2, (a.z + b.z) / 2, 0);
                        Vec3 n(0, mid.y, mid.z);
                        if (n.normalise().dot(iso.dir) > 0.3)
                            emettre_trait(items, a, b, iso, "arete");
                    }
                }
            }
        }
        // bores : cercles intérieurs au premier/dernier cap (traits seulement)
        for (double bore : bores) {
            for (double xe : {segs.front().x0, segs.back().x1}) {
                Vec3 normale(xe == segs.front().x0 ? -1.0 : 1.0, 0, 0);
                if (normale.dot(iso.dir) <= 0) continue;
                double rb = bore / 2.0;
                for (int i = 0; i < N; ++i) {
                    double t1 = 2 * PI * i / N, t2 = 2 * PI * (i + 1) / N;
                    emettre_trait(items,
                                  Vec3(xe, rb * std::cos(t1), rb * std::sin(t1)),
                                  Vec3(xe, rb * std::cos(t2), rb * std::sin(t2)),
                                  iso, "bore");
                }
            }
        }
        for (const std::string& c : cotes_du_profil(segs, bores))
            cotes.arr.push_back(JVal::texte(c));
    } else {
        err = "'type' requis : boite | cylindre | revolution";
        return false;
    }

    // Painter : liste de rendu UNIFIÉE (faces + traits) TRIÉE par profondeur
    // CROISSANTE (loin d'abord — l'itérateur dessine dans l'ordre du tableau).
    std::stable_sort(items.begin(), items.end(),
                     [](const ItemRendu& a, const ItemRendu& b) { return a.zc < b.zc; });
    JVal rendu = JVal::tableau();
    int id = 1;
    for (const auto& it : items) {
        JVal o = JVal::objet();
        o.set("id", JVal::texte("r" + std::to_string(id++)));
        o.set("type", JVal::texte(it.type));
        o.set("role", JVal::texte(it.role));
        o.set("couleur", JVal::texte(it.couleur));
        JVal pts = JVal::tableau();
        for (auto& p : it.points) {
            JVal pt = JVal::tableau();
            pt.arr.push_back(JVal::nombre(p.first));
            pt.arr.push_back(JVal::nombre(p.second));
            pts.arr.push_back(pt);
        }
        o.set("points", pts);
        o.set("z_profondeur", JVal::nombre(it.zc));
        rendu.arr.push_back(o);
    }
    double ratio_vs = iso.ratio_cap();
    double theo = std::sin(deg2rad(el));
    JVal verif = JVal::objet();
    verif.set("ratio_cap_valeurs_singulieres", JVal::nombre(ratio_vs));
    verif.set("ratio_theorique_sin_elevation", JVal::nombre(theo));
    verif.set("concordance", JVal::boo(std::fabs(ratio_vs - theo) < 1e-9));
    JVal palette = JVal::objet();
    palette.set("dessus", JVal::texte("#d8d8f8"));
    palette.set("flanc_clair", JVal::texte("#b8b8c0"));
    palette.set("flanc_sombre", JVal::texte("#a8a8b0"));
    palette.set("dessous", JVal::texte("#a0a0a8"));
    palette.set("trait", JVal::texte("#4b4b51"));
    out.set("type", JVal::texte(type));
    out.set("azimut_deg", JVal::nombre(az));
    out.set("elevation_deg", JVal::nombre(el));
    out.set("echantillons", JVal::nombre(N));
    out.set("nb_rendu", JVal::nombre(static_cast<double>(rendu.arr.size())));
    out.set("rendu", rendu);
    out.set("cotes", cotes);
    out.set("verif_perspective", verif);
    out.set("palette", palette);
    out.set("note", JVal::texte("painter : liste unifiée faces+traits triée par profondeur croissante (loin d'abord) ; faces émises seulement si normale vers la caméra (caps n′z > 0) ; arcs moitié externe par échantillonnage des secteurs visibles"));
    return true;
}

// ============================ Dispatcher ============================

static std::atomic<bool> g_demande_arret{false};
static std::atomic<int> g_clients{0};

static JVal traiter(const std::string& op, const JVal& args) {
    JVal rep = JVal::objet();
    rep.set("op", JVal::texte(op));
    if (op == "echo") {
        rep.set("ok", JVal::boo(true));
        rep.set("pong", args.has("ping") ? *args.get("ping") : args);
        rep.set("pid", JVal::nombre(static_cast<double>(::getpid())));
        rep.set("version", JVal::texte(VERSION_SCRIPT));
        rep.set("capacites", liste_capacites());
        return rep;
    }
    if (op == "daemon.stop") {
        rep.set("ok", JVal::boo(true));
        rep.set("arret", JVal::boo(true));
        rep.set("message", JVal::texte("arrêt propre demandé — socket supprimée"));
        g_demande_arret = true;
        return rep;
    }
    JVal corps = JVal::objet();
    std::string err;
    bool ok = false;
    if (op == "trig.eval") ok = op_trig_eval(args, corps, err);
    else if (op == "trig.resoudre") ok = op_trig_resoudre(args, corps, err);
    else if (op == "canonique.cercle") ok = op_canonique_cercle(args, corps, err);
    else if (op == "canonique.ellipse") ok = op_canonique_ellipse(args, corps, err);
    else if (op == "analyse.derivee") ok = op_analyse_derivee(args, corps, err);
    else if (op == "analyse.primitive") ok = op_analyse_primitive(args, corps, err);
    else if (op == "analyse.integrale") ok = op_analyse_integrale(args, corps, err);
    else if (op == "fourier.serie") ok = op_fourier_serie(args, corps, err);
    else if (op == "fourier.eval") ok = op_fourier_eval(args, corps, err);
    else if (op == "euler.formule") ok = op_euler_formule(args, corps, err);
    else if (op == "euler.rotation") ok = op_euler_rotation(args, corps, err);
    else if (op == "euler.projection") ok = op_euler_projection(args, corps, err);
    else if (op == "euler.caracteristique") ok = op_euler_caracteristique(args, corps, err);
    else if (op == "piece.profil_2d") ok = op_piece_profil_2d(args, corps, err);
    else if (op == "piece.modele_iso") ok = op_piece_modele_iso(args, corps, err);
    else {
        rep.set("ok", JVal::boo(false));
        rep.set("erreur", JVal::texte("op inconnue : " + op));
        rep.set("capacites", liste_capacites());
        return rep;
    }
    rep.set("ok", JVal::boo(ok));
    if (!ok) {
        rep.set("erreur", JVal::texte(err));
    } else {
        for (auto& p : corps.obj) rep.obj.push_back(std::move(p));
    }
    return rep;
}

static JVal traiter_requete(const JVal& req) {
    std::string op = req.get_str("op", "");
    const JVal* args = req.get("args");
    JVal vide = JVal::objet();
    return traiter(op, args ? *args : vide);
}

// ============================ Auto-diagnostic (--selftest) ============================

struct ResTest {
    std::string id, capacite, detail;
    bool pass = false;
};

static bool proche(double a, double b, double tol) { return std::fabs(a - b) <= tol; }

static void selftest() {
    std::vector<ResTest> tests;
    auto verifie = [&](const std::string& id, const std::string& cap, const JVal& rep,
                       bool cond, const std::string& detail) {
        ResTest r;
        r.id = id;
        r.capacite = cap;
        r.pass = cond && rep.get_boo("ok", false);
        r.detail = detail;
        tests.push_back(r);
    };
    {
        JVal a = JVal::objet();
        a.set("fonction", JVal::texte("sin"));
        a.set("x", JVal::nombre(0.5));
        JVal rep = traiter("trig.eval", a);
        verifie("T01", "trig.eval", rep,
                proche(rep.get_num("valeur", 0), 0.479425538604203, 1e-9),
                "sin(0.5) = " + fmt_fr(rep.get_num("valeur", 0), 12));
    }
    {
        JVal a = JVal::objet();
        a.set("oppose", JVal::nombre(3));
        a.set("adjacente", JVal::nombre(4));
        JVal rep = traiter("trig.resoudre", a);
        verifie("T02", "trig.resoudre", rep,
                proche(rep.get_num("hypotenuse", 0), 5, 1e-12) &&
                    proche(rep.get_num("angle_deg", 0), 36.86989764584402, 1e-9),
                "3-4-5 → hyp 5, angle " + fmt_fr(rep.get_num("angle_deg", 0), 6) + "°");
    }
    {
        JVal pts = JVal::tableau();
        double xy[3][2] = {{0, 0}, {4, 0}, {0, 4}};
        for (auto& p : xy) {
            JVal q = JVal::tableau();
            q.arr.push_back(JVal::nombre(p[0]));
            q.arr.push_back(JVal::nombre(p[1]));
            pts.arr.push_back(q);
        }
        JVal a = JVal::objet();
        a.set("points", pts);
        JVal rep = traiter("canonique.cercle", a);
        const JVal* c = rep.get("centre");
        verifie("T03", "canonique.cercle", rep,
                c && c->arr.size() == 2 && proche(c->arr[0].num, 2, 1e-12) &&
                    proche(c->arr[1].num, 2, 1e-12) && proche(rep.get_num("rayon", 0), 2 * std::sqrt(2), 1e-12),
                "3 points → centre (2, 2), rayon " + fmt_fr(rep.get_num("rayon", 0), 6));
    }
    {
        // Ellipse exacte a=3, b=1.5, θ=30° échantillonnée en 12 points exacts.
        JVal pts = JVal::tableau();
        double rot = deg2rad(30), A = 3, B = 1.5;
        for (int k = 0; k < 12; ++k) {
            double t = 2 * PI * k / 12;
            double xe = A * std::cos(t), ye = B * std::sin(t);
            double xr = xe * std::cos(rot) - ye * std::sin(rot);
            double yr = xe * std::sin(rot) + ye * std::cos(rot);
            JVal q = JVal::tableau();
            q.arr.push_back(JVal::nombre(xr));
            q.arr.push_back(JVal::nombre(yr));
            pts.arr.push_back(q);
        }
        JVal a = JVal::objet();
        a.set("points", pts);
        JVal rep = traiter("canonique.ellipse", a);
        bool ok = proche(rep.get_num("demi_axe_a", 0), 3.0, 1e-6) &&
                  proche(rep.get_num("demi_axe_b", 0), 1.5, 1e-6);
        double rd = rep.get_num("rotation_deg", -1);
        ok = ok && (proche(rd, 30.0, 1e-4) || proche(rd, 30.0 + 180.0, 1e-4));
        verifie("T04", "canonique.ellipse", rep, ok,
                "a = " + fmt_fr(rep.get_num("demi_axe_a", 0), 6) + ", b = " +
                    fmt_fr(rep.get_num("demi_axe_b", 0), 6) + ", rot = " + fmt_fr(rd, 4) + "°");
    }
    {
        JVal a = JVal::objet();
        a.set("fonction", JVal::texte("cos"));
        a.set("x", JVal::nombre(0.5));
        JVal rep = traiter("analyse.derivee", a);
        verifie("T05", "analyse.derivee", rep,
                proche(rep.get_num("derivee", 0), -std::sin(0.5), 1e-7),
                "d/dx cos en 0.5 = " + fmt_fr(rep.get_num("derivee", 0), 9));
    }
    {
        JVal c = JVal::tableau();
        c.arr.push_back(JVal::nombre(1));
        c.arr.push_back(JVal::nombre(2));
        c.arr.push_back(JVal::nombre(3));
        JVal a = JVal::objet();
        a.set("coefficients", c);
        JVal rep = traiter("analyse.primitive", a);
        const JVal* p = rep.get("coefficients_primitive");
        bool ok = p && p->arr.size() == 4 && proche(p->arr[1].num, 1, 1e-12) &&
                  proche(p->arr[2].num, 1, 1e-12) && proche(p->arr[3].num, 1, 1e-12);
        verifie("T06", "analyse.primitive", rep, ok,
                "∫(1+2x+3x²)dx = x + x² + x³ + C");
    }
    {
        JVal a = JVal::objet();
        a.set("fonction", JVal::texte("sin"));
        a.set("a", JVal::nombre(0));
        a.set("b", JVal::nombre(PI));
        JVal rep = traiter("analyse.integrale", a);
        verifie("T07", "analyse.integrale", rep,
                proche(rep.get_num("integrale", 0), 2.0, 1e-9),
                "∫sin sur [0, π] = " + fmt_fr(rep.get_num("integrale", 0), 12));
    }
    {
        JVal a = JVal::objet();
        a.set("fonction", JVal::texte("sin"));
        a.set("periode", JVal::nombre(2 * PI));
        a.set("harmoniques", JVal::nombre(3));
        JVal rep = traiter("fourier.serie", a);
        const JVal* an = rep.get("an");
        const JVal* bn = rep.get("bn");
        bool ok = proche(rep.get_num("a0", 1), 0, 1e-9) && an && bn &&
                  proche(bn->arr[0].num, 1, 1e-9) && proche(an->arr[0].num, 0, 1e-9) &&
                  proche(bn->arr[1].num, 0, 1e-9) && proche(bn->arr[2].num, 0, 1e-9);
        verifie("T08", "fourier.serie", rep, ok,
                "série de sin : bn[1] = " + fmt_fr(bn ? bn->arr[0].num : -1, 6));
    }
    {
        JVal an = JVal::tableau(), bn = JVal::tableau();
        an.arr.push_back(JVal::nombre(0));
        an.arr.push_back(JVal::nombre(0));
        bn.arr.push_back(JVal::nombre(1));
        bn.arr.push_back(JVal::nombre(0));
        JVal a = JVal::objet();
        a.set("a0", JVal::nombre(0));
        a.set("an", an);
        a.set("bn", bn);
        a.set("periode", JVal::nombre(2 * PI));
        a.set("x", JVal::nombre(PI / 2));
        JVal rep = traiter("fourier.eval", a);
        verifie("T09", "fourier.eval", rep,
                proche(rep.get_num("valeur", 0), 1.0, 1e-9),
                "sin(π/2) reconstruit = " + fmt_fr(rep.get_num("valeur", 0), 9));
    }
    {
        JVal a = JVal::objet();
        a.set("theta", JVal::nombre(PI / 2));
        JVal rep = traiter("euler.formule", a);
        verifie("T10", "euler.formule", rep,
                proche(rep.get_num("re", 1), 0, 1e-12) && proche(rep.get_num("im", 0), 1, 1e-12),
                "e^(iπ/2) = " + fmt_fr(rep.get_num("re", 1), 3) + " + " +
                    fmt_fr(rep.get_num("im", 0), 3) + "·i");
    }
    {
        JVal ang = JVal::tableau();
        ang.arr.push_back(JVal::nombre(90));
        ang.arr.push_back(JVal::nombre(0));
        ang.arr.push_back(JVal::nombre(0));
        JVal p = JVal::tableau();
        p.arr.push_back(JVal::nombre(1));
        p.arr.push_back(JVal::nombre(0));
        p.arr.push_back(JVal::nombre(0));
        JVal a = JVal::objet();
        a.set("angles_deg", ang);
        a.set("point", p);
        JVal rep = traiter("euler.rotation", a);
        const JVal* pt = rep.get("point_tourne");
        const JVal* q = rep.get("quaternion");
        bool ok = pt && proche(pt->arr[0].num, 0, 1e-12) && proche(pt->arr[1].num, 1, 1e-12) &&
                  proche(pt->arr[2].num, 0, 1e-12) && q &&
                  proche(q->arr[0].num, std::sqrt(0.5), 1e-12) &&
                  proche(q->arr[3].num, std::sqrt(0.5), 1e-12);
        verifie("T11", "euler.rotation", rep, ok,
                "ZXZ (90,0,0) : (1,0,0) → (0,1,0), q = [√2/2, 0, 0, √2/2]");
    }
    {
        JVal p = JVal::tableau();
        p.arr.push_back(JVal::nombre(1));
        p.arr.push_back(JVal::nombre(0));
        p.arr.push_back(JVal::nombre(0));
        JVal a = JVal::objet();
        a.set("point", p);
        JVal rep = traiter("euler.projection", a);
        const JVal* p2 = rep.get("point_2d");
        bool ok = p2 && proche(p2->arr[0].num, -std::sqrt(0.5), 1e-12) &&
                  proche(p2->arr[1].num, -0.5773502691896258 * std::sqrt(0.5), 1e-12) &&
                  rep.get_boo("concordance", false);
        verifie("T12", "euler.projection", rep, ok,
                "iso (1,0,0) → (" + fmt_fr(p2 ? p2->arr[0].num : 0, 6) + ", " +
                    fmt_fr(p2 ? p2->arr[1].num : 0, 6) + "), ratio cap concordant");
    }
    {
        JVal M = JVal::tableau();
        double c = std::cos(deg2rad(90)), s = std::sin(deg2rad(90));
        double lignes[3][3] = {{c, -s, 0}, {s, c, 0}, {0, 0, 1}};
        for (auto& li : lignes) {
            JVal l = JVal::tableau();
            for (double v : li) l.arr.push_back(JVal::nombre(v));
            M.arr.push_back(l);
        }
        JVal a = JVal::objet();
        a.set("matrice", M);
        JVal rep = traiter("euler.caracteristique", a);
        const JVal* axe = rep.get("axe");
        const JVal* q = rep.get("quaternion");
        bool ok = proche(rep.get_num("angle_deg", 0), 90, 1e-9) && axe &&
                  proche(axe->arr[2].num, 1, 1e-12) && q &&
                  proche(q->arr[0].num, std::sqrt(0.5), 1e-12) &&
                  proche(q->arr[3].num, std::sqrt(0.5), 1e-12);
        verifie("T13", "euler.caracteristique", rep, ok,
                "Rz(90°) → angle 90°, axe z, quaternion [√2/2, 0, 0, √2/2]");
    }
    {
        JVal s1 = JVal::objet();
        s1.set("x0", JVal::nombre(0));
        s1.set("x1", JVal::nombre(50));
        s1.set("d", JVal::nombre(20));
        JVal segs = JVal::tableau();
        segs.arr.push_back(s1);
        JVal a = JVal::objet();
        a.set("segments", segs);
        JVal rep = traiter("piece.profil_2d", a);
        const JVal* aires = rep.get("aires");
        const JVal* sec = rep.get("section_axiale");
        const JVal* sol = rep.get("solide");
        bool ok = aires && proche(aires->get_num("aire_mm2", 0), 500, 1e-9) && sec &&
                  proche(sec->get_num("aire_mm2", 0), 1000, 1e-9) &&
                  proche(sec->get_num("ix_autour_axe_mm4", 0), 50000.0 / 1.5, 1e-6) &&
                  sol && proche(sol->get_num("volume_guldin_mm3", 0), 5000 * PI, 1e-6);
        verifie("T14", "piece.profil_2d", rep, ok,
                "cylindre Ø20×50 : demi " + fmt_fr(aires ? aires->get_num("aire_mm2", 0) : 0, 4) +
                    " mm², V = " + fmt_fr(sol ? sol->get_num("volume_guldin_mm3", 0) : 0, 4) + " mm³ (Guldin)");
    }
    {
        JVal a = JVal::objet();
        a.set("type", JVal::texte("cylindre"));
        a.set("d", JVal::nombre(20));
        a.set("h", JVal::nombre(50));
        JVal rep = traiter("piece.modele_iso", a);
        const JVal* rendu = rep.get("rendu");
        bool tri_ok = true, dessus_ok = false;
        double zc_prev = -1e18;
        if (rendu && rendu->t == JVal::ARR && !rendu->arr.empty()) {
            for (const auto& it : rendu->arr) {
                double zc = it.get_num("z_profondeur", 0);
                if (zc < zc_prev - 1e-9) tri_ok = false;
                zc_prev = zc;
                if (it.get_str("role", "") == "dessus") dessus_ok = true;
            }
        } else {
            tri_ok = false;
        }
        const JVal* verif = rep.get("verif_perspective");
        bool ok = tri_ok && dessus_ok && verif && verif->get_boo("concordance", false) &&
                  rep.get_num("nb_rendu", 0) > 40;
        verifie("T15", "piece.modele_iso", rep, ok,
                "cylindre : " + fmt_fr(rep.get_num("nb_rendu", 0), 0) +
                    " items, tri profondeur " + (tri_ok ? "OK" : "KO") +
                    ", cap dessus visible, ratio cap concordant");
    }

    int pass = 0;
    for (auto& t : tests)
        if (t.pass) ++pass;
    for (auto& t : tests) {
        std::printf("%s %-24s %s — %s\n", t.id.c_str(), t.capacite.c_str(),
                    t.pass ? "PASS" : "FAIL", t.detail.c_str());
    }
    JVal rapport = JVal::objet();
    rapport.set("script", JVal::texte("trigo-euler"));
    rapport.set("version", JVal::texte(VERSION_SCRIPT));
    rapport.set("verdict", JVal::texte(std::to_string(pass) + "/" +
                                       std::to_string(tests.size()) + " PASS"));
    JVal arr = JVal::tableau();
    for (auto& t : tests) {
        JVal o = JVal::objet();
        o.set("id", JVal::texte(t.id));
        o.set("capacite", JVal::texte(t.capacite));
        o.set("pass", JVal::boo(t.pass));
        o.set("detail", JVal::texte(t.detail));
        arr.arr.push_back(o);
    }
    rapport.set("tests", arr);
    std::printf("%s\n", jval_dump(rapport).c_str());
    if (pass != static_cast<int>(tests.size())) std::exit(1);
}

// ============================ Daemon ============================

static volatile sig_atomic_t g_signal_stop = 0;
static void gestionnaire_signal(int) { g_signal_stop = 1; }

static bool envoyer_tout(int fd, const std::string& msg) {
    size_t total = 0;
    while (total < msg.size()) {
        ssize_t n = ::send(fd, msg.data() + total, msg.size() - total, MSG_NOSIGNAL);
        if (n <= 0) return false;
        total += static_cast<size_t>(n);
    }
    return true;
}

static void boucle_client(int fd) {
    std::string buf;
    char tmp[8192];
    while (!g_demande_arret && !g_signal_stop) {
        ssize_t n = ::recv(fd, tmp, sizeof tmp, 0);
        if (n <= 0) break;
        buf.append(tmp, static_cast<size_t>(n));
        size_t pos;
        while ((pos = buf.find('\n')) != std::string::npos) {
            std::string ligne = buf.substr(0, pos);
            buf.erase(0, pos + 1);
            // trim blancs en bouts
            while (!ligne.empty() && (ligne.back() == '\r' || ligne.back() == ' ' ||
                                      ligne.back() == '\t'))
                ligne.pop_back();
            while (!ligne.empty() && (ligne.front() == ' ' || ligne.front() == '\t'))
                ligne.erase(0, 1);
            if (ligne.empty()) continue;
            JVal req;
            std::string perr;
            JVal rep;
            if (!json_parse(ligne, req, perr)) {
                rep = JVal::objet();
                rep.set("ok", JVal::boo(false));
                rep.set("erreur", JVal::texte("json invalide : " + perr));
            } else if (req.get_str("op", "").empty()) {
                rep = JVal::objet();
                rep.set("ok", JVal::boo(false));
                rep.set("erreur", JVal::texte("champ 'op' manquant"));
            } else {
                rep = traiter_requete(req);
            }
            if (!envoyer_tout(fd, jval_dump(rep) + "\n")) {
                ::close(fd);
                g_clients--;
                return;
            }
        }
    }
    ::close(fd);
    g_clients--;
}

static int lancer_daemon(const std::string& chemin_socket, const std::string& ready_file,
                         const std::string& pid_file, int max_clients) {
    std::signal(SIGTERM, gestionnaire_signal);
    std::signal(SIGINT, gestionnaire_signal);
    std::signal(SIGPIPE, SIG_IGN);
    ::unlink(chemin_socket.c_str());
    int fd = ::socket(AF_UNIX, SOCK_STREAM, 0);
    if (fd < 0) {
        std::fprintf(stderr, "trigo-euler : socket() impossible\n");
        return 2;
    }
    sockaddr_un addr{};
    addr.sun_family = AF_UNIX;
    if (chemin_socket.size() >= sizeof addr.sun_path) {
        std::fprintf(stderr, "trigo-euler : chemin de socket trop long\n");
        return 2;
    }
    std::strncpy(addr.sun_path, chemin_socket.c_str(), sizeof addr.sun_path - 1);
    if (::bind(fd, reinterpret_cast<sockaddr*>(&addr), sizeof addr) < 0) {
        std::fprintf(stderr, "trigo-euler : bind(%s) impossible\n", chemin_socket.c_str());
        return 2;
    }
    if (::listen(fd, 16) < 0) {
        std::fprintf(stderr, "trigo-euler : listen impossible\n");
        ::unlink(chemin_socket.c_str());
        return 2;
    }
    {
        std::ofstream pf(pid_file);
        pf << ::getpid() << "\n";
        std::ofstream rf(ready_file);
        rf << ::getpid() << " " << VERSION_SCRIPT << "\n";
    }
    pollfd pfd{};
    pfd.fd = fd;
    pfd.events = POLLIN;
    while (!g_signal_stop && !g_demande_arret) {
        int r = ::poll(&pfd, 1, 100);
        if (r <= 0) continue;
        int c = ::accept(fd, nullptr, nullptr);
        if (c < 0) continue;
        if (g_clients.load() >= max_clients) {
            // Refus NON-BLOQUANT : réponse immédiate puis fermeture.
            JVal rep = JVal::objet();
            rep.set("ok", JVal::boo(false));
            rep.set("erreur", JVal::texte("daemon sature"));
            rep.set("clients", JVal::nombre(g_clients.load()));
            rep.set("max_clients", JVal::nombre(max_clients));
            envoyer_tout(c, jval_dump(rep) + "\n");
            ::close(c);
            continue;
        }
        g_clients++;
        std::thread(boucle_client, c).detach();
    }
    ::close(fd);
    ::unlink(chemin_socket.c_str());
    ::unlink(ready_file.c_str());
    ::unlink(pid_file.c_str());
    return 0;
}

// ============================ CLI ============================

static void usage() {
    std::fprintf(stderr,
        "trigo-euler v%s — moteur mathématique du skill dessin-technique\n"
        "  --selftest                          auto-diagnostic 15 capacités\n"
        "  --request F --out F                 mode one-shot (requête/réponse fichiers)\n"
        "  [--stdin]                           mode stdin (NDJSON, une requête par ligne)\n"
        "  --daemon --socket S --ready-file R --pid-file P --max-clients N\n"
        "  --version                           informations du nœud\n",
        VERSION_SCRIPT);
}

int main(int argc, char** argv) {
    std::string req_file, out_file, chemin_socket = "/tmp/trigo-euler.sock",
                                          ready_file = "/tmp/trigo-euler.ready",
                                          pid_file = "/tmp/trigo-euler.pid";
    int max_clients = 8;
    bool selftest_mode = false, daemon_mode = false, stdin_mode = false, version_mode = false,
         one_shot = false;
    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        if (a == "--selftest") selftest_mode = true;
        else if (a == "--request" && i + 1 < argc) { req_file = argv[++i]; one_shot = true; }
        else if (a == "--out" && i + 1 < argc) out_file = argv[++i];
        else if (a == "--daemon") daemon_mode = true;
        else if (a == "--stdin") stdin_mode = true;
        else if (a == "--socket" && i + 1 < argc) chemin_socket = argv[++i];
        else if (a == "--ready-file" && i + 1 < argc) ready_file = argv[++i];
        else if (a == "--pid-file" && i + 1 < argc) pid_file = argv[++i];
        else if (a == "--max-clients" && i + 1 < argc) max_clients = std::atoi(argv[++i]);
        else if (a == "--version") version_mode = true;
        else if (a == "--help" || a == "-h") { usage(); return 0; }
        else {
            std::fprintf(stderr, "argument inconnu : %s\n", a.c_str());
            usage();
            return 2;
        }
    }
    if (selftest_mode) {
        selftest();
        return 0;
    }
    if (version_mode) {
        JVal v = JVal::objet();
        v.set("script", JVal::texte("trigo-euler"));
        v.set("version", JVal::texte(VERSION_SCRIPT));
        v.set("standard", JVal::texte("C++17"));
        v.set("skill", JVal::texte("dessin-technique"));
        v.set("capacites", liste_capacites());
        v.set("compilation", JVal::texte("g++ -O2 -std=c++17 -pthread -Wall"));
        std::printf("%s\n", jval_dump(v).c_str());
        return 0;
    }
    if (daemon_mode) {
        if (max_clients < 1) max_clients = 8;
        return lancer_daemon(chemin_socket, ready_file, pid_file, max_clients);
    }
    if (one_shot) {
        if (req_file.empty() || out_file.empty()) {
            std::fprintf(stderr, "--request et --out requis ensemble\n");
            return 2;
        }
        std::ifstream in(req_file);
        if (!in) {
            std::fprintf(stderr, "lecture impossible : %s\n", req_file.c_str());
            return 2;
        }
        std::stringstream ss;
        ss << in.rdbuf();
        JVal req;
        std::string perr;
        if (!json_parse(ss.str(), req, perr)) {
            JVal rep = JVal::objet();
            rep.set("ok", JVal::boo(false));
            rep.set("erreur", JVal::texte("json invalide : " + perr));
            std::ofstream outf(out_file);
            outf << jval_dump(rep) << "\n";
            return 1;
        }
        JVal rep = traiter_requete(req);
        std::ofstream outf(out_file);
        outf << jval_dump(rep) << "\n";
        return rep.get_boo("ok", false) ? 0 : 1;
    }
    // mode stdin par défaut : NDJSON (une requête par ligne, une réponse par ligne)
    (void)stdin_mode;
    std::string ligne;
    while (std::getline(std::cin, ligne)) {
        while (!ligne.empty() && (ligne.back() == '\r' || ligne.back() == ' '))
            ligne.pop_back();
        if (ligne.empty()) continue;
        JVal req;
        std::string perr;
        JVal rep;
        if (!json_parse(ligne, req, perr)) {
            rep = JVal::objet();
            rep.set("ok", JVal::boo(false));
            rep.set("erreur", JVal::texte("json invalide : " + perr));
        } else {
            rep = traiter_requete(req);
        }
        std::printf("%s\n", jval_dump(rep).c_str());
        std::fflush(stdout);
    }
    return 0;
}
