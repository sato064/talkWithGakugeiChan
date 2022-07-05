"""
__author__ = "sato064, hanehaneland"
"""
from transformers import T5Tokenizer, AutoModelForCausalLM
import torch
from collections import defaultdict
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from typing import Dict
from transformers import pipeline 
from transformers import AutoModelForSequenceClassification 
from transformers import BertJapaneseTokenizer 
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello Fast API"}

@app.post("/")
async def post(item: Dict):
    text = item["msg"]
    print(text)
    
    retext = ''

    hash = lambda: defaultdict(hash)
    dic = hash()
    dic['学芸大丼'] = '学芸大丼は量が多いです….'
    dic['櫨山研究室'] = '櫨山研究室はソフトウェア開発が盛んですね. 情報教育専修でもプログラミングに特化した研究室です.'
    dic['宮寺研究室'] = '宮寺研究室は情報理論の研究室ですよね．'
    dic['森本研究室'] = '森本研はいつ見ても電気がついていますね.遅くまでお疲れ様です.'
    dic['加藤研究室'] = '加藤研究室は，情報教育専修の中ではHCIの研究が盛んですね.　常に教育のICT化を考えて工夫する方法を考えています.'
    dic['サークル棟'] = 'サークル棟…すごく古い建物ですよね.　入ったことはないのですが汚いというウワサも…'
    dic['櫨山'] = '櫨山先生,普段は優しい先生ですね.　でも授業評価の採点基準は厳しいです.'
    dic['宮寺'] = '宮寺先生はとっつきづらそうな雰囲気はありますが,話してみると優しくてよく笑ってくれる先生ですよ.'
    dic['絵'] = '私は絵を描くのが苦手です.　ネットスラングでいう画伯…でしょうか'
    dic['ソーラン節'] = 'どっこいしょーどっこいしょー　ソーランソーラン… はっ！ついソーラン節を聞くと踊ってしまいますね.　あなたも一緒にどうですか？'
    dic['python'] = 'python好きーーーーっっ！ 私の心はpythonで書かれています．'


    bi_hash = lambda: defaultdict(bi_hash)
    bi_dic = bi_hash()
    bi_dic['学芸大']['特徴'] = '学芸大は，こんな名前だけど国立大学なんですよ． 実は武蔵小金井のほうが近いんですよね． こんなやつが教壇に立って良いのかと思うやつが多々いるって誰かが言ってました． 実は学芸大学駅から遠いのですよ．'
    bi_dic['学芸大']['体育'] = '学芸大の体育だとボウリングが楽しいって噂ですよね．'
    bi_dic['学芸大']['学務課'] = '学芸大の学務課は閉まるのが早いですよね． たしか16:15とか．'
    bi_dic['学芸大']['守衛'] = '学芸大って学生証なくても入れます？'
    bi_dic['学芸大']['駅'] = '学芸大って駅から遠いですよね…'
    bi_dic['学芸大']['オタク'] = '学芸大のオタクはしぶんけんに集まってます．'
    bi_dic['学食']['おすすめ'] = '学芸大の学食のおすすめは味噌バターコーンラーメンですっ！あと，カレーもおいしいですよね．'
    bi_dic['櫨山研究室']['特徴'] = '櫨山研究室はみんな仲がいいですね.いつも和気藹々とした雰囲気だと思います.'
    bi_dic['好き']['食べ物'] = '私の好きな食べ物はラーメンですね.　学芸大だと味噌バターコーンラーメン！やっぱりアレが一番ですね！'
    bi_dic['好き']['星座'] = '私の星座は獅子座です.　学芸大学のシンボルでもあるんですよ.'
    bi_dic['好き']['飲み物'] = '私の好きな飲み物はココアです.　甘いものも好きで,中でもココアは別格です.　温めても冷ましてもおいしいのがいいですよね.'


    tri_hash = lambda: defaultdict(tri_hash)
    tri_dic = tri_hash()
    tri_dic['学芸大']['おすすめ']['場所'] = '学芸大で好きな場所と言えば…農場です．'
    tri_dic['学芸大']['建物']['高い'] = '学芸で高い建物は，サンシャインですよねっ！'

    for word in dic:
        if word in text:
            # print('確認', dic.get(word))
            retext = retext + dic.get(word)

    for word in bi_dic:
        for sub_word in bi_dic[word]:
            if word in text and sub_word in text:
                # print('確認', bi_dic[word].get(sub_word))
                retext = retext + bi_dic[word].get(sub_word)

    for word in tri_dic:
        for sub_word in tri_dic[word]:
            for subsub_word in tri_dic[word][sub_word]:
                if word in text and sub_word in text and subsub_word in text:
                    # print('確認', tri_dic[word][sub_word].get(subsub_word))
                    retext = retext + tri_dic[word][sub_word].get(subsub_word)

    if not retext:
        retext = text
    # print('確認 retextは', retext)

    # トークナイザーとモデルの準備
    tokenizer = T5Tokenizer.from_pretrained("rinna/japanese-gpt-1b")
    model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-1b")

    # 続きを生成したいテキスト
    text = retext

    # テキストのエンコード
    token_ids = tokenizer.encode(text, add_special_tokens=False, return_tensors="pt")

    # 文章生成
    with torch.no_grad():
        output_ids = model.generate(
            token_ids,
            do_sample=True,
            max_length=100,
            min_length=30,
            top_k=50,
            top_p=0.92,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            bad_word_ids=[[tokenizer.unk_token_id]]
        )

    # テキストのデコード
    sentences = tokenizer.batch_decode(output_ids.tolist())

    print(sentences)
    s_stc = ""
    for sentence in sentences:
        s_stc = s_stc + sentence
    print(s_stc)

    d = {'msg' : s_stc.replace("</s>","")}

    model = AutoModelForSequenceClassification.from_pretrained('daigo/bert-base-japanese-sentiment') 
    tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking') 
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer) 
    print(nlp(text)[0]["label"])
    print(nlp(text)[0]["score"])
    if nlp(text)[0]["label"] == 'ポジティブ':
        if nlp(text)[0]["score"] > 0.986:
            d['emt'] = 'banzai'
        elif nlp(text)[0]["score"] > 0.95:
            d['emt'] = 'yatta'
        else:
            d['emt'] = 'uresi'
    else:
        if nlp(text)[0]["score"] > 0.98:
            d['emt'] = 'oko'
        else:
            d['emt'] = 'un'
    
    json_obj = json.dumps(d, ensure_ascii=False)
    
    return d
