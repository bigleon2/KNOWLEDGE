'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Brain, Search, Plus, Pin, PinOff, Trash2, Edit3, X,
  Database, Users, Zap, Shield, Target, BookOpen, Settings,
  Sparkles, RefreshCw, Tag,
  Minus, Hash, Clock, Star, Cpu,
  AlertTriangle, Circle, Save, Wrench, Key, Copy, Pencil
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

// Types
interface KnowledgeEntry {
  id: string
  title: string
  content: string
  category: string
  tags: string
  priority: string
  source: string
  pinned: boolean
  createdAt: string
  updatedAt: string
}

interface Stats {
  total: number
  pinned: number
  categories: Record<string, number>
  priorities: Record<string, number>
}

// Category config
const CATEGORIES = [
  { key: 'all', label: 'Tout', icon: Database, color: 'text-slate-500' },
  { key: 'profile', label: 'Profil', icon: Users, color: 'text-violet-500' },
  { key: 'agent', label: 'Agents', icon: Cpu, color: 'text-emerald-500' },
  { key: 'skill', label: 'Skills', icon: Zap, color: 'text-amber-500' },
  { key: 'protocol', label: 'Protocoles', icon: Shield, color: 'text-rose-500' },
  { key: 'trigger', label: 'Déclencheurs', icon: Target, color: 'text-cyan-500' },
  { key: 'rule', label: 'Règles', icon: BookOpen, color: 'text-orange-500' },
  { key: 'other', label: 'Autres', icon: Settings, color: 'text-gray-500' },
]

const PRIORITY_CONFIG: Record<string, { label: string; icon: typeof AlertTriangle; color: string; bg: string }> = {
  critical: { label: 'Critique', icon: AlertTriangle, color: 'text-red-600', bg: 'bg-red-50 border-red-200' },
  important: { label: 'Important', icon: Star, color: 'text-amber-600', bg: 'bg-amber-50 border-amber-200' },
  normal: { label: 'Normal', icon: Circle, color: 'text-blue-600', bg: 'bg-blue-50 border-blue-200' },
  secondary: { label: 'Secondaire', icon: Minus, color: 'text-gray-500', bg: 'bg-gray-50 border-gray-200' },
}

// Config types
interface ConfigEntry {
  id: string
  key: string
  value: string
  category: string
  description: string
  createdAt: string
  updatedAt: string
}

const CONFIG_CATEGORIES = [
  { key: 'all', label: 'Tout', color: 'text-slate-500' },
  { key: 'profile', label: 'Profil', color: 'text-violet-500' },
  { key: 'ecosystem', label: 'Écosystème', color: 'text-emerald-500' },
  { key: 'gen-plan', label: 'Gen-Plan', color: 'text-rose-500' },
  { key: 'decision', label: 'Décision', color: 'text-amber-500' },
  { key: 'rules', label: 'Règles', color: 'text-orange-500' },
  { key: 'app', label: 'App', color: 'text-cyan-500' },
  { key: 'config', label: 'Config', color: 'text-gray-500' },
]

export default function KnowledgePage() {
  const [entries, setEntries] = useState<KnowledgeEntry[]>([])
  const [stats, setStats] = useState<Stats | null>(null)
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [seeded, setSeeded] = useState(false)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingEntry, setEditingEntry] = useState<KnowledgeEntry | null>(null)
  const [viewingEntry, setViewingEntry] = useState<KnowledgeEntry | null>(null)
  const [activeTab, setActiveTab] = useState('grid')
  const [mainTab, setMainTab] = useState<'knowledge' | 'config'>('knowledge')

  // Config state
  const [configs, setConfigs] = useState<ConfigEntry[]>([])
  const [configCategory, setConfigCategory] = useState('all')
  const [editingConfig, setEditingConfig] = useState<ConfigEntry | null>(null)
  const [configDialogOpen, setConfigDialogOpen] = useState(false)
  const [configFormKey, setConfigFormKey] = useState('')
  const [configFormValue, setConfigFormValue] = useState('')
  const [configFormCategory, setConfigFormCategory] = useState('config')
  const [configFormDescription, setConfigFormDescription] = useState('')

  // Form state
  const [formTitle, setFormTitle] = useState('')
  const [formContent, setFormContent] = useState('')
  const [formCategory, setFormCategory] = useState('other')
  const [formTags, setFormTags] = useState('')
  const [formPriority, setFormPriority] = useState('normal')

  const loadData = async (category: string, search: string, doSeed = false) => {
    try {
      if (doSeed) {
        const seedRes = await fetch('/api/knowledge/seed', { method: 'POST' })
        const seedData = await seedRes.json()
        if (seedData.count > 0) {
          setSeeded(true)
        }
      }

      const params = new URLSearchParams()
      if (category !== 'all') params.set('category', category)
      if (search) params.set('search', search)

      const [entriesRes, statsRes] = await Promise.all([
        fetch(`/api/knowledge?${params.toString()}`),
        fetch('/api/knowledge/stats'),
      ])

      const entriesData = await entriesRes.json()
      const statsData = await statsRes.json()

      setEntries(entriesData)
      setStats(statsData)
      if (!doSeed) setSeeded(true)
    } catch (err) {
      console.error('Error loading data:', err)
    }
  }

  // Initial load
  useEffect(() => {
    const init = async () => {
      setLoading(true)
      const res = await fetch('/api/knowledge')
      const data = await res.json()
      if (data.length === 0) {
        await loadData('all', '', true)
      } else {
        await loadData('all', '', false)
      }
      setLoading(false)
    }
    init()
  }, [])

  // Refresh when category or search changes
  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category)
    loadData(category, searchQuery)
  }

  const handleSearchChange = (value: string) => {
    setSearchQuery(value)
    loadData(selectedCategory, value)
  }

  const refreshData = () => {
    loadData(selectedCategory, searchQuery)
    if (mainTab === 'config') loadConfigs()
  }

  // Config data loading
  const loadConfigs = async () => {
    try {
      const params = new URLSearchParams()
      if (configCategory !== 'all') params.set('category', configCategory)
      const res = await fetch(`/api/config?${params.toString()}`)
      const data = await res.json()
      setConfigs(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error('Error loading configs:', err)
    }
  }

  const seedConfigs = async () => {
    try {
      const res = await fetch('/api/config/seed', { method: 'POST' })
      const data = await res.json()
      if (data.count > 0) loadConfigs()
    } catch (err) {
      console.error('Error seeding configs:', err)
    }
  }

  useEffect(() => {
    if (mainTab === 'config') loadConfigs()
  }, [mainTab, configCategory])

  const handleConfigSave = async () => {
    if (!configFormKey || !configFormValue) return
    try {
      if (editingConfig) {
        await fetch('/api/config', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ key: editingConfig.key, value: configFormValue, category: configFormCategory, description: configFormDescription }),
        })
      } else {
        await fetch('/api/config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ key: configFormKey, value: configFormValue, category: configFormCategory, description: configFormDescription }),
        })
      }
      setConfigDialogOpen(false)
      resetConfigForm()
      loadConfigs()
    } catch (err) {
      console.error('Error saving config:', err)
    }
  }

  const handleConfigDelete = async (key: string) => {
    try {
      await fetch(`/api/config?key=${encodeURIComponent(key)}`, { method: 'DELETE' })
      loadConfigs()
    } catch (err) {
      console.error('Error deleting config:', err)
    }
  }

  const openConfigEditDialog = (config: ConfigEntry) => {
    setEditingConfig(config)
    setConfigFormKey(config.key)
    setConfigFormValue(config.value)
    setConfigFormCategory(config.category)
    setConfigFormDescription(config.description)
    setConfigDialogOpen(true)
  }

  const openConfigNewDialog = () => {
    setEditingConfig(null)
    resetConfigForm()
    setConfigDialogOpen(true)
  }

  const resetConfigForm = () => {
    setConfigFormKey('')
    setConfigFormValue('')
    setConfigFormCategory('config')
    setConfigFormDescription('')
    setEditingConfig(null)
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
  }

  const handleSave = async () => {
    if (!formTitle || !formContent) return

    try {
      if (editingEntry) {
        await fetch('/api/knowledge', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id: editingEntry.id,
            title: formTitle,
            content: formContent,
            category: formCategory,
            tags: formTags,
            priority: formPriority,
          }),
        })
      } else {
        await fetch('/api/knowledge', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            title: formTitle,
            content: formContent,
            category: formCategory,
            tags: formTags,
            priority: formPriority,
            source: 'manual',
          }),
        })
      }

      setDialogOpen(false)
      resetForm()
      refreshData()
    } catch (err) {
      console.error('Error saving entry:', err)
    }
  }

  const handleDelete = async (id: string) => {
    try {
      await fetch(`/api/knowledge?id=${id}`, { method: 'DELETE' })
      refreshData()
      if (viewingEntry?.id === id) setViewingEntry(null)
    } catch (err) {
      console.error('Error deleting entry:', err)
    }
  }

  const handleTogglePin = async (entry: KnowledgeEntry) => {
    try {
      await fetch('/api/knowledge', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: entry.id, pinned: !entry.pinned }),
      })
      refreshData()
    } catch (err) {
      console.error('Error toggling pin:', err)
    }
  }

  const openEditDialog = (entry: KnowledgeEntry) => {
    setEditingEntry(entry)
    setFormTitle(entry.title)
    setFormContent(entry.content)
    setFormCategory(entry.category)
    setFormTags(entry.tags)
    setFormPriority(entry.priority)
    setDialogOpen(true)
  }

  const openNewDialog = () => {
    setEditingEntry(null)
    resetForm()
    setDialogOpen(true)
  }

  const resetForm = () => {
    setFormTitle('')
    setFormContent('')
    setFormCategory('other')
    setFormTags('')
    setFormPriority('normal')
    setEditingEntry(null)
  }

  const getCategoryInfo = (key: string) => CATEGORIES.find(c => c.key === key) || CATEGORIES[CATEGORIES.length - 1]
  const getPriorityInfo = (key: string) => PRIORITY_CONFIG[key] || PRIORITY_CONFIG.normal

  const pinnedEntries = entries.filter(e => e.pinned)
  const unpinnedEntries = entries.filter(e => !e.pinned)

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          className="w-12 h-12 rounded-full border-4 border-primary border-t-transparent"
        />
      </div>
    )
  }

  return (
    <TooltipProvider>
      <div className="min-h-screen bg-background flex flex-col">
        {/* Header */}
        <header className="border-b border-border bg-card/80 backdrop-blur-sm sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg">
                {mainTab === 'knowledge' ? <Brain className="w-6 h-6 text-white" /> : <Wrench className="w-6 h-6 text-white" />}
              </div>
              <div>
                <h1 className="text-xl font-bold tracking-tight">KNOWLEDGE</h1>
                <p className="text-xs text-muted-foreground">{mainTab === 'knowledge' ? 'Mémoire persistante — Connaissances' : 'Mémoire persistante — Configs'}</p>
              </div>
            </div>

            <div className="flex items-center gap-2 sm:gap-3">
              {/* Main tab toggle */}
              <div className="flex items-center bg-muted rounded-lg p-0.5">
                <button
                  onClick={() => setMainTab('knowledge')}
                  className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${mainTab === 'knowledge' ? 'bg-background shadow text-foreground' : 'text-muted-foreground hover:text-foreground'}`}
                >
                  <span className="flex items-center gap-1.5"><Brain className="w-3.5 h-3.5" /> <span className="hidden sm:inline">Connaissances</span></span>
                </button>
                <button
                  onClick={() => setMainTab('config')}
                  className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${mainTab === 'config' ? 'bg-background shadow text-foreground' : 'text-muted-foreground hover:text-foreground'}`}
                >
                  <span className="flex items-center gap-1.5"><Wrench className="w-3.5 h-3.5" /> <span className="hidden sm:inline">Config</span></span>
                </button>
              </div>

              {mainTab === 'knowledge' ? (
                <>
              {/* Search */}
              <div className="relative hidden sm:block">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  placeholder="Rechercher..."
                  value={searchQuery}
                  onChange={(e) => handleSearchChange(e.target.value)}
                  className="pl-9 w-48 md:w-64 h-9"
                />
              </div>

              {/* Mobile search */}
              <Dialog>
                <DialogTrigger asChild>
                  <Button variant="ghost" size="icon" className="sm:hidden">
                    <Search className="w-4 h-4" />
                  </Button>
                </DialogTrigger>
                <DialogContent className="sm:max-w-md">
                  <DialogHeader>
                    <DialogTitle>Rechercher</DialogTitle>
                  </DialogHeader>
                  <Input
                    placeholder="Rechercher dans la base..."
                    value={searchQuery}
                    onChange={(e) => handleSearchChange(e.target.value)}
                    className="w-full"
                    autoFocus
                  />
                </DialogContent>
              </Dialog>
                </>
              ) : null}

              <Tooltip>
                <TooltipTrigger asChild>
                  <Button variant="ghost" size="icon" onClick={refreshData}>
                    <RefreshCw className="w-4 h-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Actualiser</TooltipContent>
              </Tooltip>

              {mainTab === 'knowledge' ? (
                <Button onClick={openNewDialog} size="sm" className="gap-2">
                  <Plus className="w-4 h-4" />
                  <span className="hidden sm:inline">Ajouter</span>
                </Button>
              ) : (
                <Button onClick={openConfigNewDialog} size="sm" className="gap-2">
                  <Plus className="w-4 h-4" />
                  <span className="hidden sm:inline">Config</span>
                </Button>
              )}
            </div>
          </div>
        </header>

        <div className="flex-1 flex">
          {/* Sidebar */}
          <aside className="hidden lg:flex w-56 border-r border-border bg-card/50 flex-col">
            <div className="p-4">
              <h2 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">Categories</h2>
              <nav className="space-y-1">
                {CATEGORIES.map((cat) => {
                  const Icon = cat.icon
                  const count = cat.key === 'all'
                    ? (stats?.total || 0)
                    : (stats?.categories[cat.key] || 0)
                  return (
                    <button
                      key={cat.key}
                      onClick={() => handleCategoryChange(cat.key)}
                      className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-colors ${
                        selectedCategory === cat.key
                          ? 'bg-primary text-primary-foreground font-medium'
                          : 'hover:bg-accent text-foreground'
                      }`}
                    >
                      <Icon className={`w-4 h-4 ${selectedCategory === cat.key ? 'text-primary-foreground' : cat.color}`} />
                      <span className="flex-1 text-left">{cat.label}</span>
                      <Badge variant="secondary" className="text-xs h-5 min-w-[20px] justify-center">
                        {count}
                      </Badge>
                    </button>
                  )
                })}
              </nav>
            </div>

            <Separator className="mx-4" />

            {/* Stats */}
            {stats && (
              <div className="p-4 space-y-3">
                <h2 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Statistiques</h2>
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Total</span>
                    <span className="font-semibold">{stats.total}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Épinglés</span>
                    <span className="font-semibold">{stats.pinned}</span>
                  </div>
                  {Object.entries(stats.priorities).map(([key, count]) => {
                    const info = PRIORITY_CONFIG[key]
                    if (!info) return null
                    return (
                      <div key={key} className="flex items-center justify-between text-sm">
                        <span className={`flex items-center gap-1.5 ${info.color}`}>
                          <info.icon className="w-3 h-3" />
                          {info.label}
                        </span>
                        <span className="font-semibold">{count as number}</span>
                      </div>
                    )
                  })}
                </div>
              </div>
            )}

            <div className="mt-auto p-4">
              <div className="rounded-lg bg-gradient-to-br from-emerald-500/10 to-teal-500/10 border border-emerald-500/20 p-3">
                <div className="flex items-center gap-2 mb-1">
                  <Sparkles className="w-4 h-4 text-emerald-500" />
                  <span className="text-xs font-semibold text-emerald-700 dark:text-emerald-400">Memoire active</span>
                </div>
                <p className="text-xs text-muted-foreground">
                  12 agents · 71 skills · gen-plan v1.0.0
                </p>
              </div>
            </div>
          </aside>

          {/* Main Content */}
          <main className="flex-1 overflow-hidden">
          {mainTab === 'knowledge' ? (
            <>
            {/* Mobile category tabs */}
            <div className="lg:hidden border-b border-border bg-card/50 overflow-x-auto">
              <div className="flex items-center gap-1 px-4 py-2">
                {CATEGORIES.map((cat) => {
                  const Icon = cat.icon
                  return (
                    <button
                      key={cat.key}
                      onClick={() => handleCategoryChange(cat.key)}
                      className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs whitespace-nowrap transition-colors ${
                        selectedCategory === cat.key
                          ? 'bg-primary text-primary-foreground font-medium'
                          : 'bg-accent text-foreground'
                      }`}
                    >
                      <Icon className="w-3 h-3" />
                      {cat.label}
                    </button>
                  )
                })}
              </div>
            </div>

            <ScrollArea className="h-[calc(100vh-8rem)] lg:h-[calc(100vh-5rem)]">
              <div className="max-w-5xl mx-auto p-4 sm:p-6 space-y-6">
                {/* Stats Cards (mobile friendly) */}
                {stats && (
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0 }}>
                      <Card className="border-l-4 border-l-violet-500">
                        <CardContent className="p-3 sm:p-4">
                          <div className="flex items-center gap-2">
                            <Users className="w-4 h-4 text-violet-500" />
                            <span className="text-xs text-muted-foreground">Profil</span>
                          </div>
                          <p className="text-2xl font-bold mt-1">{stats.categories.profile || 0}</p>
                        </CardContent>
                      </Card>
                    </motion.div>
                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }}>
                      <Card className="border-l-4 border-l-emerald-500">
                        <CardContent className="p-3 sm:p-4">
                          <div className="flex items-center gap-2">
                            <Cpu className="w-4 h-4 text-emerald-500" />
                            <span className="text-xs text-muted-foreground">Agents</span>
                          </div>
                          <p className="text-2xl font-bold mt-1">{stats.categories.agent || 0}</p>
                        </CardContent>
                      </Card>
                    </motion.div>
                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
                      <Card className="border-l-4 border-l-rose-500">
                        <CardContent className="p-3 sm:p-4">
                          <div className="flex items-center gap-2">
                            <Shield className="w-4 h-4 text-rose-500" />
                            <span className="text-xs text-muted-foreground">Protocoles</span>
                          </div>
                          <p className="text-2xl font-bold mt-1">{stats.categories.protocol || 0}</p>
                        </CardContent>
                      </Card>
                    </motion.div>
                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}>
                      <Card className="border-l-4 border-l-orange-500">
                        <CardContent className="p-3 sm:p-4">
                          <div className="flex items-center gap-2">
                            <BookOpen className="w-4 h-4 text-orange-500" />
                            <span className="text-xs text-muted-foreground">Regles</span>
                          </div>
                          <p className="text-2xl font-bold mt-1">{stats.categories.rule || 0}</p>
                        </CardContent>
                      </Card>
                    </motion.div>
                  </div>
                )}

                {/* View Toggle */}
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-lg font-semibold">
                      {selectedCategory === 'all' ? 'Toutes les entrees' : getCategoryInfo(selectedCategory).label}
                    </h2>
                    <p className="text-sm text-muted-foreground">
                      {entries.length} entree{entries.length !== 1 ? 's' : ''} trouvee{entries.length !== 1 ? 's' : ''}
                    </p>
                  </div>
                  <Tabs value={activeTab} onValueChange={setActiveTab}>
                    <TabsList className="h-8">
                      <TabsTrigger value="grid" className="text-xs px-2.5">Grille</TabsTrigger>
                      <TabsTrigger value="list" className="text-xs px-2.5">Liste</TabsTrigger>
                    </TabsList>
                  </Tabs>
                </div>

                {/* Pinned Section */}
                {pinnedEntries.length > 0 && (
                  <div className="space-y-3">
                    <div className="flex items-center gap-2 text-sm font-medium text-amber-600 dark:text-amber-400">
                      <Pin className="w-4 h-4" />
                      Epinglees
                    </div>
                    <div className={activeTab === 'grid'
                      ? 'grid grid-cols-1 md:grid-cols-2 gap-4'
                      : 'space-y-3'
                    }>
                      <AnimatePresence>
                        {pinnedEntries.map((entry, i) => (
                          <motion.div
                            key={entry.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            transition={{ delay: i * 0.03 }}
                          >
                            <KnowledgeCard
                              entry={entry}
                              view={activeTab}
                              onEdit={openEditDialog}
                              onDelete={handleDelete}
                              onTogglePin={handleTogglePin}
                              onView={setViewingEntry}
                              getCategoryInfo={getCategoryInfo}
                              getPriorityInfo={getPriorityInfo}
                              formatDate={formatDate}
                            />
                          </motion.div>
                        ))}
                      </AnimatePresence>
                    </div>
                  </div>
                )}

                {/* Unpinned Entries */}
                {unpinnedEntries.length > 0 && (
                  <div className="space-y-3">
                    {pinnedEntries.length > 0 && (
                      <Separator />
                    )}
                    <div className={activeTab === 'grid'
                      ? 'grid grid-cols-1 md:grid-cols-2 gap-4'
                      : 'space-y-3'
                    }>
                      <AnimatePresence>
                        {unpinnedEntries.map((entry, i) => (
                          <motion.div
                            key={entry.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            transition={{ delay: i * 0.02 }}
                          >
                            <KnowledgeCard
                              entry={entry}
                              view={activeTab}
                              onEdit={openEditDialog}
                              onDelete={handleDelete}
                              onTogglePin={handleTogglePin}
                              onView={setViewingEntry}
                              getCategoryInfo={getCategoryInfo}
                              getPriorityInfo={getPriorityInfo}
                              formatDate={formatDate}
                            />
                          </motion.div>
                        ))}
                      </AnimatePresence>
                    </div>
                  </div>
                )}

                {entries.length === 0 && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-center py-16"
                  >
                    <Brain className="w-16 h-16 text-muted-foreground/30 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-muted-foreground">Aucune entree trouvee</h3>
                    <p className="text-sm text-muted-foreground mt-1">
                      {searchQuery ? 'Essayez une autre recherche' : 'Ajoutez votre premiere entree'}
                    </p>
                  </motion.div>
                )}
              </div>
            </ScrollArea>
            </>
          ) : (
            /* ═══ CONFIG PANEL ═══ */
            <ScrollArea className="h-[calc(100vh-5rem)]">
              <div className="max-w-5xl mx-auto p-4 sm:p-6 space-y-6">
                {/* Config category filter */}
                <div className="flex items-center gap-2 overflow-x-auto pb-2">
                  {CONFIG_CATEGORIES.map((cat) => (
                    <button
                      key={cat.key}
                      onClick={() => setConfigCategory(cat.key)}
                      className={`px-3 py-1.5 rounded-full text-xs whitespace-nowrap transition-colors ${configCategory === cat.key ? 'bg-primary text-primary-foreground font-medium' : 'bg-accent text-foreground'}`}
                    >
                      {cat.label}
                    </button>
                  ))}
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-lg font-semibold">Configurations</h2>
                    <p className="text-sm text-muted-foreground">{configs.length} config{configs.length !== 1 ? 's' : ''}</p>
                  </div>
                  {configs.length === 0 && (
                    <Button onClick={seedConfigs} size="sm" variant="outline" className="gap-2">
                      <Database className="w-4 h-4" />
                      Initialiser les configs
                    </Button>
                  )}
                </div>

                {/* Config table */}
                {configs.length > 0 ? (
                  <div className="rounded-lg border border-border overflow-hidden">
                    <div className="bg-muted/50 px-4 py-2.5 grid grid-cols-[1fr_2fr_1fr] gap-4 text-xs font-semibold text-muted-foreground">
                      <span>Clé</span>
                      <span>Valeur</span>
                      <span className="text-right">Actions</span>
                    </div>
                    <div className="divide-y divide-border">
                      {configs.map((config, i) => (
                        <motion.div
                          key={config.id}
                          initial={{ opacity: 0, y: 5 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: i * 0.02 }}
                          className="px-4 py-3 grid grid-cols-[1fr_2fr_1fr] gap-4 items-center hover:bg-muted/30 transition-colors"
                        >
                          <div>
                            <div className="flex items-center gap-1.5">
                              <Key className="w-3 h-3 text-muted-foreground" />
                              <span className="font-mono text-sm font-medium">{config.key}</span>
                            </div>
                            {config.description && (
                              <p className="text-xs text-muted-foreground mt-0.5">{config.description}</p>
                            )}
                          </div>
                          <div className="flex items-center gap-2">
                            <code className="text-xs bg-muted px-2 py-1 rounded flex-1 truncate">{config.value}</code>
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button variant="ghost" size="icon" className="h-7 w-7 flex-shrink-0" onClick={() => copyToClipboard(config.value)}>
                                  <Copy className="w-3.5 h-3.5" />
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>Copier</TooltipContent>
                            </Tooltip>
                          </div>
                          <div className="flex items-center justify-end gap-1">
                            <Badge variant="outline" className="text-[10px]">{config.category}</Badge>
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => openConfigEditDialog(config)}>
                                  <Pencil className="w-3.5 h-3.5" />
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>Modifier</TooltipContent>
                            </Tooltip>
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button variant="ghost" size="icon" className="h-7 w-7 text-destructive" onClick={() => handleConfigDelete(config.key)}>
                                  <Trash2 className="w-3.5 h-3.5" />
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>Supprimer</TooltipContent>
                            </Tooltip>
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <Wrench className="w-12 h-12 text-muted-foreground/30 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-muted-foreground">Aucune configuration</h3>
                    <p className="text-sm text-muted-foreground mt-1">Cliquez sur "Initialiser les configs" pour charger les valeurs par défaut</p>
                  </div>
                )}
              </div>
            </ScrollArea>
          )}
          </main>
        </div>

        {/* Add/Edit Dialog */}
        <Dialog open={dialogOpen} onOpenChange={(open) => {
          setDialogOpen(open)
          if (!open) resetForm()
        }}>
          <DialogContent className="sm:max-w-lg max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2">
                {editingEntry ? (
                  <><Edit3 className="w-5 h-5" /> Modifier l&apos;entree</>
                ) : (
                  <><Plus className="w-5 h-5" /> Nouvelle entree</>
                )}
              </DialogTitle>
            </DialogHeader>

            <div className="space-y-4 py-2">
              <div className="space-y-2">
                <label className="text-sm font-medium">Titre</label>
                <Input
                  placeholder="Titre de l'entree..."
                  value={formTitle}
                  onChange={(e) => setFormTitle(e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Contenu</label>
                <Textarea
                  placeholder="Contenu de la connaissance..."
                  value={formContent}
                  onChange={(e) => setFormContent(e.target.value)}
                  rows={6}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Categorie</label>
                  <Select value={formCategory} onValueChange={setFormCategory}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="profile">Profil</SelectItem>
                      <SelectItem value="agent">Agent</SelectItem>
                      <SelectItem value="skill">Skill</SelectItem>
                      <SelectItem value="protocol">Protocole</SelectItem>
                      <SelectItem value="trigger">Declencheur</SelectItem>
                      <SelectItem value="rule">Regle</SelectItem>
                      <SelectItem value="other">Autre</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium">Priorite</label>
                  <Select value={formPriority} onValueChange={setFormPriority}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="critical">Critique</SelectItem>
                      <SelectItem value="important">Important</SelectItem>
                      <SelectItem value="normal">Normal</SelectItem>
                      <SelectItem value="secondary">Secondaire</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Tags (separes par virgules)</label>
                <Input
                  placeholder="tag1, tag2, tag3..."
                  value={formTags}
                  onChange={(e) => setFormTags(e.target.value)}
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <Button variant="outline" onClick={() => { setDialogOpen(false); resetForm() }}>
                  Annuler
                </Button>
                <Button onClick={handleSave} disabled={!formTitle || !formContent} className="gap-2">
                  <Save className="w-4 h-4" />
                  {editingEntry ? 'Mettre a jour' : 'Creer'}
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>

        {/* View Entry Dialog */}
        <Dialog open={!!viewingEntry} onOpenChange={(open) => { if (!open) setViewingEntry(null) }}>
          <DialogContent className="sm:max-w-lg max-h-[90vh] overflow-y-auto">
            {viewingEntry && (
              <>
                <DialogHeader>
                  <DialogTitle className="flex items-center gap-2">
                    {(() => {
                      const catInfo = getCategoryInfo(viewingEntry.category)
                      const CatIcon = catInfo.icon
                      return <CatIcon className={`w-5 h-5 ${catInfo.color}`} />
                    })()}
                    {viewingEntry.title}
                  </DialogTitle>
                </DialogHeader>

                <div className="space-y-4 py-2">
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="outline" className={getPriorityInfo(viewingEntry.priority).color}>
                      {getPriorityInfo(viewingEntry.priority).label}
                    </Badge>
                    <Badge variant="outline">
                      {getCategoryInfo(viewingEntry.category).label}
                    </Badge>
                    {viewingEntry.source === 'imported' && (
                      <Badge variant="secondary" className="gap-1">
                        <Database className="w-3 h-3" />
                        Importe
                      </Badge>
                    )}
                    {viewingEntry.pinned && (
                      <Badge className="bg-amber-100 text-amber-700 gap-1">
                        <Pin className="w-3 h-3" />
                        Epinglee
                      </Badge>
                    )}
                  </div>

                  <div className="bg-muted/50 rounded-lg p-4">
                    <pre className="whitespace-pre-wrap text-sm leading-relaxed font-sans">
                      {viewingEntry.content}
                    </pre>
                  </div>

                  {viewingEntry.tags && (
                    <div className="flex flex-wrap gap-1.5">
                      {viewingEntry.tags.split(',').map((tag, i) => (
                        <Badge key={i} variant="secondary" className="text-xs gap-1">
                          <Hash className="w-2.5 h-2.5" />
                          {tag.trim()}
                        </Badge>
                      ))}
                    </div>
                  )}

                  <div className="flex items-center gap-4 text-xs text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      Cree: {formatDate(viewingEntry.createdAt)}
                    </span>
                    <span className="flex items-center gap-1">
                      <RefreshCw className="w-3 h-3" />
                      Modifie: {formatDate(viewingEntry.updatedAt)}
                    </span>
                  </div>

                  <Separator />

                  <div className="flex justify-end gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleTogglePin(viewingEntry)}
                      className="gap-1.5"
                    >
                      {viewingEntry.pinned ? <PinOff className="w-4 h-4" /> : <Pin className="w-4 h-4" />}
                      {viewingEntry.pinned ? 'Desepingler' : 'Epingler'}
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => { openEditDialog(viewingEntry); setViewingEntry(null) }}
                      className="gap-1.5"
                    >
                      <Edit3 className="w-4 h-4" />
                      Modifier
                    </Button>
                  </div>
                </div>
              </>
            )}
          </DialogContent>
        </Dialog>

        {/* Config Add/Edit Dialog */}
        <Dialog open={configDialogOpen} onOpenChange={(open) => {
          setConfigDialogOpen(open)
          if (!open) resetConfigForm()
        }}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2">
                {editingConfig ? (
                  <><Pencil className="w-5 h-5" /> Modifier la config</>
                ) : (
                  <><Plus className="w-5 h-5" /> Nouvelle config</>
                )}
              </DialogTitle>
            </DialogHeader>
            <div className="space-y-4 py-2">
              <div className="space-y-2">
                <label className="text-sm font-medium">Clé</label>
                <Input
                  placeholder="ex: user.name"
                  value={configFormKey}
                  onChange={(e) => setConfigFormKey(e.target.value)}
                  disabled={!!editingConfig}
                  className="font-mono"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Valeur</label>
                <Textarea
                  placeholder="Valeur de la configuration..."
                  value={configFormValue}
                  onChange={(e) => setConfigFormValue(e.target.value)}
                  rows={3}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Catégorie</label>
                <Select value={configFormCategory} onValueChange={setConfigFormCategory}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="profile">Profil</SelectItem>
                    <SelectItem value="ecosystem">Écosystème</SelectItem>
                    <SelectItem value="gen-plan">Gen-Plan</SelectItem>
                    <SelectItem value="decision">Décision</SelectItem>
                    <SelectItem value="rules">Règles</SelectItem>
                    <SelectItem value="app">App</SelectItem>
                    <SelectItem value="config">Config</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Description</label>
                <Input
                  placeholder="Description de cette config..."
                  value={configFormDescription}
                  onChange={(e) => setConfigFormDescription(e.target.value)}
                />
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <Button variant="outline" onClick={() => { setConfigDialogOpen(false); resetConfigForm() }}>
                  Annuler
                </Button>
                <Button onClick={handleConfigSave} disabled={!configFormKey || !configFormValue} className="gap-2">
                  <Save className="w-4 h-4" />
                  {editingConfig ? 'Mettre à jour' : 'Créer'}
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>

        {/* Footer */}
        <footer className="border-t border-border bg-card/80 py-3 px-4 text-center text-xs text-muted-foreground">
          KNOWLEDGE v1.0.0 — Memoire persistante pour François — 12 agents · 71 skills · gen-plan
        </footer>
      </div>
    </TooltipProvider>
  )
}

// Knowledge Card Component
function KnowledgeCard({
  entry,
  view,
  onEdit,
  onDelete,
  onTogglePin,
  onView,
  getCategoryInfo,
  getPriorityInfo,
  formatDate,
}: {
  entry: KnowledgeEntry
  view: string
  onEdit: (entry: KnowledgeEntry) => void
  onDelete: (id: string) => void
  onTogglePin: (entry: KnowledgeEntry) => void
  onView: (entry: KnowledgeEntry | null) => void
  getCategoryInfo: (key: string) => typeof CATEGORIES[number]
  getPriorityInfo: (key: string) => typeof PRIORITY_CONFIG[string]
  formatDate: (date: string) => string
}) {
  const catInfo = getCategoryInfo(entry.category)
  const CatIcon = catInfo.icon
  const priorityInfo = getPriorityInfo(entry.priority)
  const PriorityIcon = priorityInfo.icon

  if (view === 'list') {
    return (
      <Card
        className={`border-l-4 cursor-pointer transition-all hover:shadow-md ${priorityInfo.bg}`}
        onClick={() => onView(entry)}
      >
        <CardContent className="p-3 sm:p-4 flex items-center gap-3">
          <CatIcon className={`w-5 h-5 flex-shrink-0 ${catInfo.color}`} />
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <span className="font-medium text-sm truncate">{entry.title}</span>
              {entry.pinned && <Pin className="w-3 h-3 text-amber-500 flex-shrink-0" />}
            </div>
            <p className="text-xs text-muted-foreground truncate mt-0.5">{entry.content.substring(0, 80)}...</p>
          </div>
          <Badge variant="outline" className={`text-xs flex-shrink-0 ${priorityInfo.color}`}>
            {priorityInfo.label}
          </Badge>
          <div className="flex items-center gap-1 flex-shrink-0" onClick={(e) => e.stopPropagation()}>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => onTogglePin(entry)}>
                  {entry.pinned ? <PinOff className="w-3.5 h-3.5" /> : <Pin className="w-3.5 h-3.5" />}
                </Button>
              </TooltipTrigger>
              <TooltipContent>{entry.pinned ? 'Desepingler' : 'Epingler'}</TooltipContent>
            </Tooltip>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => onEdit(entry)}>
                  <Edit3 className="w-3.5 h-3.5" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>Modifier</TooltipContent>
            </Tooltip>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" className="h-7 w-7 text-destructive" onClick={() => onDelete(entry.id)}>
                  <Trash2 className="w-3.5 h-3.5" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>Supprimer</TooltipContent>
            </Tooltip>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card
      className={`cursor-pointer transition-all hover:shadow-md border-t-2 ${priorityInfo.bg}`}
      onClick={() => onView(entry)}
    >
      <CardHeader className="pb-2 px-4 pt-4">
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-center gap-2 min-w-0">
            <CatIcon className={`w-4 h-4 flex-shrink-0 ${catInfo.color}`} />
            <CardTitle className="text-sm font-semibold truncate">{entry.title}</CardTitle>
          </div>
          <div className="flex items-center gap-1 flex-shrink-0" onClick={(e) => e.stopPropagation()}>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => onTogglePin(entry)}>
                  {entry.pinned ? <PinOff className="w-3 h-3" /> : <Pin className="w-3 h-3" />}
                </Button>
              </TooltipTrigger>
              <TooltipContent>{entry.pinned ? 'Desepingler' : 'Epingler'}</TooltipContent>
            </Tooltip>
          </div>
        </div>
      </CardHeader>
      <CardContent className="px-4 pb-4 space-y-3">
        <p className="text-xs text-muted-foreground line-clamp-3 leading-relaxed">
          {entry.content}
        </p>

        <div className="flex flex-wrap gap-1.5">
          <Badge variant="outline" className={`text-[10px] ${priorityInfo.color}`}>
            <PriorityIcon className="w-2.5 h-2.5 mr-0.5" />
            {priorityInfo.label}
          </Badge>
          <Badge variant="outline" className="text-[10px]">
            {catInfo.label}
          </Badge>
          {entry.tags && entry.tags.split(',').slice(0, 2).map((tag, i) => (
            <Badge key={i} variant="secondary" className="text-[10px]">
              #{tag.trim()}
            </Badge>
          ))}
          {entry.tags && entry.tags.split(',').length > 2 && (
            <Badge variant="secondary" className="text-[10px]">
              +{entry.tags.split(',').length - 2}
            </Badge>
          )}
        </div>

        <div className="flex items-center justify-between">
          <span className="text-[10px] text-muted-foreground">
            {formatDate(entry.updatedAt)}
          </span>
          <div className="flex items-center gap-0.5" onClick={(e) => e.stopPropagation()}>
            <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => onEdit(entry)}>
              <Edit3 className="w-3 h-3" />
            </Button>
            <Button variant="ghost" size="icon" className="h-6 w-6 text-destructive" onClick={() => onDelete(entry.id)}>
              <Trash2 className="w-3 h-3" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
