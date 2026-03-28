import json
import time
import random
from datetime import datetime
from typing import Dict, List, Any

# 模拟调用大模型API的函数（实际项目中替换为真实API调用）
def call_gpt4_api(prompt: str, resume_data: Dict, job_data: Dict) -> Dict[str, Any]:
    """
    模拟GPT-4 API调用，返回匹配结果
    实际项目中应替换为真实的API调用逻辑
    """
    # 模拟API调用延迟
    time.sleep(0.1)
    
    # 模拟匹配算法：基于技能匹配度和经验年限计算得分
    resume_skills = set(resume_data.get("skills", []))
    job_skills = set(job_data.get("required_skills", []))
    
    # 计算技能匹配度
    if len(job_skills) > 0:
        skill_match_ratio = len(resume_skills & job_skills) / len(job_skills)
    else:
        skill_match_ratio = 0
    
    # 计算经验匹配度
    exp_match = min(resume_data.get("experience_years", 0) / max(job_data.get("min_experience", 1), 1), 1.5)
    
    # 综合得分（0-100分）
    score = min(100, int((skill_match_ratio * 0.7 + min(exp_match, 1) * 0.3) * 100))
    
    # 生成评估理由
    reasons = []
    if skill_match_ratio >= 0.8:
        reasons.append("技能匹配度很高")
    elif skill_match_ratio >= 0.5:
        reasons.append("技能部分匹配")
    else:
        reasons.append("技能匹配度不足")
    
    if exp_match >= 1:
        reasons.append("经验年限符合要求")
    elif exp_match >= 0.5:
        reasons.append("经验年限基本符合")
    else:
        reasons.append("经验年限不足")
    
    # 初筛决策
    decision = "推荐" if score >= 60 else "待定" if score >= 40 else "不推荐"
    
    return {
        "match_score": score,
        "decision": decision,
        "reasons": reasons,
        "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def load_sample_data() -> tuple[List[Dict], List[Dict]]:
    """加载示例简历和职位数据"""
    # 示例简历数据
    resumes = [
        {
            "id": "RES001",
            "name": "张三",
            "experience_years": 3,
            "skills": ["Python", "机器学习", "数据分析", "SQL", "PyTorch"],
            "education": "本科",
            "current_title": "AI工程师"
        },
        {
            "id": "RES002",
            "name": "李四",
            "experience_years": 1,
            "skills": ["Java", "Spring", "MySQL", "JavaScript"],
            "education": "硕士",
            "current_title": "后端开发"
        },
        {
            "id": "RES003",
            "name": "王五",
            "experience_years": 5,
            "skills": ["Python", "深度学习", "TensorFlow", "NLP", "大数据"],
            "education": "博士",
            "current_title": "算法专家"
        }
    ]
    
    # 示例职位数据
    jobs = [
        {
            "id": "JOB001",
            "title": "AI产品实习生",
            "company": "悦途",
            "required_skills": ["Python", "机器学习", "数据分析", "沟通能力"],
            "min_experience": 1,
            "location": "北京"
        },
        {
            "id": "JOB002",
            "title": "高级算法工程师",
            "company": "科技公司",
            "required_skills": ["深度学习", "PyTorch", "NLP", "Python", "大数据"],
            "min_experience": 3,
            "location": "上海"
        }
    ]
    
    return resumes, jobs

def process_resume_matching(resumes: List[Dict], jobs: List[Dict]) -> List[Dict]:
    """处理简历与职位的匹配"""
    results = []
    
    print("开始智能匹配与初筛...")
    print(f"待处理简历数: {len(resumes)}, 职位数: {len(jobs)}")
    print("-" * 50)
    
    for job in jobs:
        print(f"\n正在处理职位: {job['title']} @ {job['company']}")
        print(f"职位要求: {', '.join(job['required_skills'])}")
        
        for resume in resumes:
            # 调用模拟的GPT-4 API进行匹配
            match_result = call_gpt4_api(
                prompt=f"评估简历{resume['id']}与职位{job['id']}的匹配度",
                resume_data=resume,
                job_data=job
            )
            
            # 构建结果记录
            result = {
                "job_id": job["id"],
                "job_title": job["title"],
                "resume_id": resume["id"],
                "candidate_name": resume["name"],
                "match_score": match_result["match_score"],
                "decision": match_result["decision"],
                "reasons": match_result["reasons"],
                "processed_time": match_result["processed_at"]
            }
            
            results.append(result)
            
            # 输出匹配结果
            print(f"  候选人: {resume['name']} ({resume['current_title']})")
            print(f"  匹配分数: {match_result['match_score']}/100 | 初筛结果: {match_result['decision']}")
            print(f"  评估理由: {', '.join(match_result['reasons'])}")
    
    return results

def save_results(results: List[Dict], filename: str = "matching_results.json"):
    """保存匹配结果到JSON文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n匹配结果已保存到: {filename}")

def generate_summary_report(results: List[Dict]):
    """生成匹配结果摘要报告"""
    total_matches = len(results)
    recommended = sum(1 for r in results if r["decision"] == "推荐")
    pending = sum(1 for r in results if r["decision"] == "待定")
    not_recommended = sum(1 for r in results if r["decision"] == "不推荐")
    
    print("\n" + "=" * 50)
    print("智能招聘助手 - 匹配结果摘要报告")
    print("=" * 50)
    print(f"总匹配次数: {total_matches}")
    print(f"推荐简历: {recommended} ({recommended/total_matches*100:.1f}%)")
    print(f"待定简历: {pending} ({pending/total_matches*100:.1f}%)")
    print(f"不推荐简历: {not_recommended} ({not_recommended/total_matches*100:.1f}%)")
    
    # 找出最佳匹配
    if results:
        best_match = max(results, key=lambda x: x["match_score"])
        print(f"\n最佳匹配: {best_match['candidate_name']} -> {best_match['job_title']}")
        print(f"匹配分数: {best_match['match_score']}/100")

def main():
    """主函数：智能招聘助手入口"""
    print("智能招聘助手 v1.0")
    print("=" * 50)
    
    # 1. 加载示例数据
    resumes, jobs = load_sample_data()
    
    # 2. 处理简历匹配与初筛
    results = process_resume_matching(resumes, jobs)
    
    # 3. 保存结果
    save_results(results)
    
    # 4. 生成摘要报告
    generate_summary_report(results)
    
    print("\n处理完成！通过AI智能匹配，可显著提升筛选效率。")

if __name__ == "__main__":
    main()