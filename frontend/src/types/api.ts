/**
 * API 类型定义
 * 所有 API 请求/响应类型
 */

// ============== 通用 ==============

export interface ApiResponse<T = any> {
  code: number
  message: string
  data?: T
}

export interface PageParams {
  page?: number
  page_size?: number
}

// ============== 图片相关 ==============

export interface ImageUploadResponse {
  image_id: string
  filename: string
  url: string
  size: number
  width: number
  height: number
}

export interface BoundingBox {
  x1: number
  y1: number
  x2: number
  y2: number
}

export interface PreprocessOperation {
  type: string
  params: Record<string, any>
}

export interface PreprocessResponse {
  image_id: string
  processed_url: string
  operations: PreprocessOperation[]
}

// ============== 识别相关 ==============

export interface TextRegion {
  region_id: string
  text: string
  bbox: BoundingBox
  confidence: number
}

export interface FormulaRegion {
  region_id: string
  latex: string
  bbox: BoundingBox
  confidence: number
}

export interface DiagramObject {
  type: string
  label?: string
  bbox?: BoundingBox
}

export interface ForceInfo {
  name: string
  on: string
  direction: string
  magnitude?: string
  bbox?: BoundingBox
}

export interface DiagramAnnotation {
  text: string
  position: { x: number; y: number }
}

export interface DiagramElements {
  objects: DiagramObject[]
  forces: ForceInfo[]
  annotations: DiagramAnnotation[]
}

export interface SegmentResponse {
  image_id: string
  regions: Array<{
    region_id: string
    type: 'text' | 'formula' | 'diagram'
    bbox: BoundingBox
    confidence: number
  }>
}

export interface OCRResponse {
  image_id: string
  text_regions: TextRegion[]
}

export interface FormulaResponse {
  image_id: string
  formula_regions: FormulaRegion[]
}

// ============== 标准答案相关 ==============

export interface AnswerStep {
  order: number
  description: string
  content: string
  formula?: string
  score: number
}

export interface StandardAnswer {
  answer_id: string
  question_title: string
  subject: string
  grade: string
  chapter: string
  steps: AnswerStep[]
  total_score: number
  tags?: string[]
  created_at?: string
}

export interface StandardAnswerCreate {
  question_title: string
  subject?: string
  grade?: string
  chapter: string
  steps: AnswerStep[]
  total_score?: number
  tags?: string[]
}

export interface StandardAnswerListResponse {
  total: number
  page: number
  page_size: number
  items: StandardAnswer[]
}

// ============== 批改相关 ==============

export interface GradingSubmitRequest {
  image_id: string
  standard_answer_id: string
  options?: {
    include_diagram?: boolean
    detail_level?: 'simple' | 'detailed'
  }
}

export interface StepGradingResult {
  step: number
  description: string
  student_answer: string
  is_correct: boolean
  score: number
  max_score: number
  comment?: string
}

export interface GradingSubmitResponse {
  grading_id: string
  image_id: string
  standard_answer_id: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  total_score: number
  max_score: number
  processing_time: number
  created_at: string
}

export interface GradingStatus {
  grading_id: string
  status: string
  progress: number
  steps: Array<{
    step: string
    status: 'pending' | 'processing' | 'completed' | 'failed'
    time?: number
  }>
}

export interface GradingResultResponse {
  grading_id: string
  total_score: number
  max_score: number
  step_results: StepGradingResult[]
  feedback: string
  suggestions?: string[]
}

// ============== 班级相关 ==============

export interface ClassInfo {
  class_id: string
  class_name: string
  grade: string
  description?: string
  student_count: number
  teacher: {
    user_id: number
    username: string
  }
  created_at?: string
}

export interface StudentSummary {
  student_name: string
  grading_count: number
  average_score: number
  latest_grading_id?: string
}

export interface ClassSummary {
  class_id: string
  class_name: string
  grading_count: number
  average_score: number
  pass_rate: number
  students: StudentSummary[]
}

// ============== 历史记录 ==============

export interface HistoryItem {
  grading_id: string
  image_id: string
  student_name?: string
  standard_answer_id: string
  question_title: string
  total_score: number
  max_score: number
  created_at: string
}

export interface HistoryListResponse {
  total: number
  page: number
  page_size: number
  items: HistoryItem[]
}

// ============== 批量处理 ==============

export interface BatchCreate {
  class_id?: string
  image_ids: string[]
  standard_answer_id: string
}

export interface BatchResponse {
  batch_id: string
  total: number
  pending: number
  completed: number
  failed: number
  status: string
  created_at?: string
}
