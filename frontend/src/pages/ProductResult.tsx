// Sonuç sayfası: kopyalanabilir görsel prompt + SEO metin kartları.
import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Link, useParams } from 'react-router-dom'
import { api } from '../lib/api'
import type { Product } from '../lib/types'
import { PageLoader, BouncingBlocks } from '../components/Loader'
import ErrorAlert from '../components/ErrorAlert'

function CopyButton({ text, label }: { text: string; label?: string }) {
  const [copied, setCopied] = useState(false)

  async function copy() {
    await navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 1800)
  }

  return (
    <motion.button
      whileTap={{ scale: 0.94 }}
      onClick={copy}
      className={`rounded-lg border-2 border-ink px-3 py-1.5 text-xs font-bold uppercase tracking-wider transition-colors ${
        copied ? 'bg-lime text-ink' : 'bg-lemon text-ink hover:bg-lemon-dark'
      }`}
    >
      {copied ? '✓ Kopyalandı' : (label ?? 'Kopyala')}
    </motion.button>
  )
}

export default function ProductResult() {
  const { id } = useParams()
  const [product, setProduct] = useState<Product | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [regenerating, setRegenerating] = useState(false)
  const [imageUrl, setImageUrl] = useState<string | null>(null)
  const [imageLoading, setImageLoading] = useState(false)

  useEffect(() => {
    api
      .getProduct(Number(id))
      .then(setProduct)
      .catch((err) => setError(err.message))
  }, [id])

  useEffect(() => {
    if (!product) return

    let revoked = false
    let currentUrl: string | null = null

    setImageLoading(true)
    api
      .getProductImage(product.id)
      .then((blob) => {
        currentUrl = URL.createObjectURL(blob)
        if (!revoked) setImageUrl(currentUrl)
      })
      .catch((err) => setError(err.message))
      .finally(() => setImageLoading(false))

    return () => {
      revoked = true
      if (currentUrl) URL.revokeObjectURL(currentUrl)
    }
  }, [product])

  async function regenerate() {
    if (!product) return
    setError(null)
    setRegenerating(true)
    try {
      const result = await api.generate(product.id)
      setProduct(result.product)
      setImageUrl(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Üretim başarısız oldu.')
    } finally {
      setRegenerating(false)
    }
  }

  if (error && !product) {
    return (
      <div className="mx-auto max-w-xl px-4 py-16">
        <ErrorAlert message={error} />
        <Link to="/dashboard" className="btn-white mt-6">
          ← Panele Dön
        </Link>
      </div>
    )
  }

  if (!product) return <PageLoader label="Ürün yükleniyor" />

  const keywords =
    product.uretilen_anahtar_kelimeler?.split(',').map((k) => k.trim()) ?? []
  const hasResults = Boolean(product.uretilen_gorsel_prompt)

  const KEYWORD_COLORS = [
    'bg-pink text-white',
    'bg-lemon text-ink',
    'bg-claude text-white',
    'bg-lime text-ink',
    'bg-electric text-white',
  ]

  return (
    <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <Link
            to="/dashboard"
            className="text-sm font-bold uppercase tracking-widest text-ink/50 hover:text-pink"
          >
            ← Panele dön
          </Link>
          <h1 className="mt-2 font-display text-3xl font-bold tracking-tight sm:text-4xl">
            {product.uretilen_baslik ?? `${product.renk} ${product.kategori}`}
          </h1>
          <p className="mt-1 font-medium text-ink/60">
            {product.materyal} · {product.tarz} · {product.renk} ·{' '}
            {product.hedef_kitle}
          </p>
        </div>
        <button onClick={regenerate} disabled={regenerating} className="btn-lemon">
          {regenerating ? 'Üretiliyor…' : hasResults ? '↻ Yeniden Üret' : '✦ Üret'}
        </button>
      </div>

      <div className="mt-6">
        <ErrorAlert message={error} />
      </div>

      {regenerating && (
        <div className="card-brutal mt-8 flex flex-col items-center gap-4 bg-gradient-to-br from-lemon/30 to-pink/10 p-10">
          <BouncingBlocks label="Ajanlar çalışıyor" />
        </div>
      )}

      {!hasResults && !regenerating && (
        <div className="card-brutal mt-8 bg-lemon/30 p-10 text-center">
          <p className="text-4xl">🎬</p>
          <p className="mt-3 font-display text-xl font-bold">
            Bu ürün için henüz içerik üretilmedi.
          </p>
          <p className="mt-1 font-medium text-ink/60">
            "Üret" butonuna bas; ajanlar sahne alsın.
          </p>
        </div>
      )}

      {hasResults && !regenerating && (
        <div className="mt-8 space-y-6">
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card-brutal mx-auto w-full max-w-2xl overflow-hidden"
          >
            <div className="flex items-center justify-between border-b-[3px] border-ink bg-ink px-5 py-3">
              <h2 className="font-display font-bold uppercase tracking-widest text-lemon">
                🖼️ Üretilen Görsel
              </h2>
            </div>
            <div className="bg-white p-4 sm:p-5">
              {imageLoading && !imageUrl ? (
                <div className="flex min-h-[200px] items-center justify-center rounded-xl border-2 border-dashed border-ink/20 bg-ink/5">
                  <BouncingBlocks label="Görsel yükleniyor" />
                </div>
              ) : imageUrl ? (
                <img
                  src={imageUrl}
                  alt={product.uretilen_baslik ?? product.kategori}
                  className="mx-auto max-h-[320px] w-auto max-w-full rounded-xl border-2 border-ink object-contain shadow-[8px_8px_0_0_#111]"
                />
              ) : (
                <div className="flex min-h-[200px] items-center justify-center rounded-xl border-2 border-dashed border-ink/20 bg-ink/5">
                  <p className="font-medium text-ink/60">
                    Görsel henüz hazırlanmadı.
                  </p>
                </div>
              )}
            </div>
          </motion.section>

          {/* Görsel Prompt — code block */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card-brutal overflow-hidden"
          >
            <div className="flex items-center justify-between border-b-[3px] border-ink bg-ink px-5 py-3">
              <h2 className="font-display font-bold uppercase tracking-widest text-lemon">
                🎨 Görsel Üretim Promptu
              </h2>
              <CopyButton text={product.uretilen_gorsel_prompt!} />
            </div>
            <pre className="whitespace-pre-wrap bg-ink/95 p-5 font-mono text-sm leading-relaxed text-lime">
              {product.uretilen_gorsel_prompt}
            </pre>
          </motion.section>

          {/* Başlık */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="card-brutal bg-gradient-to-r from-pink/10 to-electric/10 p-6"
          >
            <div className="flex items-center justify-between gap-3">
              <h2 className="font-display text-sm font-bold uppercase tracking-widest text-ink/50">
                ✍️ SEO Başlığı
              </h2>
              <CopyButton text={product.uretilen_baslik ?? ''} />
            </div>
            <p className="mt-3 font-display text-2xl font-bold leading-snug">
              {product.uretilen_baslik}
            </p>
          </motion.section>

          {/* Açıklama */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.18 }}
            className="card-brutal p-6"
          >
            <div className="flex items-center justify-between gap-3">
              <h2 className="font-display text-sm font-bold uppercase tracking-widest text-ink/50">
                📝 Ürün Açıklaması
              </h2>
              <CopyButton text={product.uretilen_aciklama ?? ''} />
            </div>
            <p className="mt-3 whitespace-pre-wrap font-medium leading-relaxed text-ink/80">
              {product.uretilen_aciklama}
            </p>
          </motion.section>

          {/* Anahtar Kelimeler */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.26 }}
            className="card-brutal bg-gradient-to-br from-lemon/30 to-lime/10 p-6"
          >
            <div className="flex items-center justify-between gap-3">
              <h2 className="font-display text-sm font-bold uppercase tracking-widest text-ink/50">
                🔑 Anahtar Kelimeler
              </h2>
              <CopyButton text={keywords.join(', ')} label="Tümünü Kopyala" />
            </div>
            <div className="mt-4 flex flex-wrap gap-2">
              {keywords.map((keyword, i) => (
                <motion.span
                  key={keyword}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.3 + i * 0.07 }}
                  className={`rounded-full border-2 border-ink px-4 py-1.5 text-sm font-bold ${
                    KEYWORD_COLORS[i % KEYWORD_COLORS.length]
                  }`}
                >
                  {keyword}
                </motion.span>
              ))}
            </div>
          </motion.section>
        </div>
      )}
    </div>
  )
}
