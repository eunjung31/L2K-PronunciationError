. ./path.sh

align-text --special-symbol="***" ark:ref ark:hyp ark,t:- | utils/scoring/wer_per_utt_details.pl --special-symbol="***" > per_utt
