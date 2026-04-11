/**
 * API 服务层
 * 封装所有后端 API 调用
 */

import axios, { AxiosError } from 'axios'
import type {
  ApiResponse,
  ImageUploadResponse,
  PreprocessResponse,
  SegmentResponse,
  OCRResponse,
  FormulaResponse,
  StandardAnswer,
  StandardAnswerCreate,
  StandardAnswerListResponse,
  GradingSubmitRequest,
  GradingSubmitResponse,
  GradingStatus,
  GradingResultResponse,
  HistoryListResponse,
  ClassInfo,
  ClassSummary,
  BatchCreate,
  BatchResponse,
} from '@/types/api'

// 创建 axios 实例
const api = axios.create({
  baseURL: '/api/v1',
  timeout: 60000, // 批改可能需要较长时间
})

// 请求拦截器：添加 token
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器：统一错误处理
api.interceptors.response.use(
  response => response.data,
  (error: AxiosError<{ detail?: string }>) => {
    const message = error.response?.data?.detail || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

// ============== 图片相关 API ==============

/**
 * 上传图片
 */
export async function uploadImage(file: File): Promise<ApiResponse<ImageUploadResponse>> {
  const formData = new FormData()
  formData.append('file', file)

  return api.post('/images/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

/**
 * 获取图片信息
 */
export async function getImage(imageId: string): Promise<ApiResponse<ImageUploadResponse>> {
  return api.get(`/images/${imageId}`)
}

/**
 * 预处理图片
 */
export async function preprocessImage(imageId: string): Promise<ApiResponse<PreprocessResponse>> {
  return api.post(`/images/${imageId}/preprocess`)
}

// ============== 识别相关 API ==============

/**
 * 图像区域分割
 */
export async function segmentRegions(imageId: string): Promise<ApiResponse<SegmentResponse>> {
  return api.post('/recognition/segment', { image_id: imageId })
}

/**
 * OCR 文字识别
 */
export async function recognizeText(imageId: string): Promise<ApiResponse<OCRResponse>> {
  return api.post('/recognition/ocr', { image_id: imageId })
}

/**
 * 公式识别
 */
export async function recognizeFormula(imageId: string): Promise<ApiResponse<FormulaResponse>> {
  return api.post('/recognition/formula', { image_id: imageId })
}

/**
 * 图形元素检测
 */
export async function detectDiagram(
  imageId: string,
  diagramType: string = 'force'
): Promise<ApiResponse<any>> {
  return api.post('/recognition/diagram', { image_id: imageId, diagram_type: diagramType })
}

/**
 * 多模态整合
 */
export async function mergeMultimodal(imageId: string): Promise<ApiResponse<any>> {
  return api.post('/recognition/merge', { image_id: imageId })
}

// ============== 标准答案 API ==============

/**
 * 获取标准答案列表
 */
export async function getAnswers(
  params?: { page?: number; page_size?: number }
): Promise<ApiResponse<StandardAnswerListResponse>> {
  return api.get('/answers', { params })
}

/**
 * 获取单个标准答案
 */
export async function getAnswer(answerId: string): Promise<ApiResponse<StandardAnswer>> {
  return api.get(`/answers/${answerId}`)
}

/**
 * 创建标准答案
 */
export async function createAnswer(
  data: StandardAnswerCreate
): Promise<ApiResponse<StandardAnswer>> {
  return api.post('/answers', data)
}

/**
 * 更新标准答案
 */
export async function updateAnswer(
  answerId: string,
  data: Partial<StandardAnswerCreate>
): Promise<ApiResponse<StandardAnswer>> {
  return api.put(`/answers/${answerId}`, data)
}

/**
 * 删除标准答案
 */
export async function deleteAnswer(answerId: string): Promise<ApiResponse<null>> {
  return api.delete(`/answers/${answerId}`)
}

// ============== 批改相关 API ==============

/**
 * 提交批改
 */
export async function submitGrading(
  data: GradingSubmitRequest
): Promise<ApiResponse<GradingSubmitResponse>> {
  return api.post('/grading/submit', data)
}

/**
 * 获取批改状态
 */
export async function getGradingStatus(
  gradingId: string
): Promise<ApiResponse<GradingStatus>> {
  return api.get(`/grading/${gradingId}/status`)
}

/**
 * 获取批改结果
 */
export async function getGradingResult(
  gradingId: string
): Promise<ApiResponse<GradingResultResponse>> {
  return api.get(`/grading/${gradingId}/result`)
}

// ============== 班级相关 API ==============

/**
 * 获取班级列表
 */
export async function getClasses(): Promise<ApiResponse<ClassInfo[]>> {
  return api.get('/classes')
}

/**
 * 获取班级详情
 */
export async function getClass(classId: string): Promise<ApiResponse<ClassInfo>> {
  return api.get(`/classes/${classId}`)
}

/**
 * 获取班级汇总
 */
export async function getClassSummary(
  classId: string
): Promise<ApiResponse<ClassSummary>> {
  return api.get(`/classes/${classId}/summary`)
}

// ============== 历史记录 API ==============

/**
 * 获取历史记录
 */
export async function getHistory(
  params?: { page?: number; page_size?: number }
): Promise<ApiResponse<HistoryListResponse>> {
  return api.get('/history', { params })
}

/**
 * 获取单条历史记录
 */
export async function getHistoryItem(
  gradingId: string
): Promise<ApiResponse<GradingResultResponse>> {
  return api.get(`/history/${gradingId}`)
}

// ============== 批量处理 API ==============

/**
 * 创建批量任务
 */
export async function createBatchTask(
  data: BatchCreate
): Promise<ApiResponse<BatchResponse>> {
  return api.post('/batch', data)
}

/**
 * 获取批量任务状态
 */
export async function getBatchStatus(
  batchId: string
): Promise<ApiResponse<BatchResponse>> {
  return api.get(`/batch/${batchId}/status`)
}

// ============== 导出默认实例 ==============
export default api
