# Teacher Candidate Quality Report

Input: `data/rulefaith/teacher_candidates_qwen_small_pilot.jsonl`

## Summary

- `candidate_count`: 160
- `provider_counts`: {'qwen_small': 160}
- `teacher_model_counts`: {'Qwen/Qwen2.5-0.5B-Instruct': 160}
- `candidate_type_counts`: {'natural': 80, 'rule_grounded': 80}
- `parse_status_counts`: {'parsed_json': 156, 'wrapped_non_json_response': 4}
- `generic_count`: 0
- `prompt_contamination_count`: 0
- `source_copy_like_count`: 0
- `too_short_count`: 4
- `low_quality_count`: 4
- `low_quality_rate`: 0.025

## Highest-Risk Examples

- `rf-edit-0199::qwen_small::rule_grounded`: ```json
{
  "edit_description": "Replace 'at' with 'in' at source token span [8,9).",
  "edit_validity": "acceptable_alternative",
  "rule_id": "1",
  "rule_text": "replace 'at' with 'in'",
  "evidence_spans": [
    {
      "text": "In my c
- `rf-edit-0231::qwen_small::natural`: ```json
{
  "edit_description": "Replace 'should' with 'is to' at source token span [1,2).",
  "edit_validity": "acceptable_alternative",
  "rule_id": "1",
  "rule_text": "Replace 'should' with 'is to'",
  "evidence_spans": [
    {
      "t
- `rf-edit-0264::qwen_small::rule_grounded`: ```json
{
  "edit_description": "Replace 'at' with 'in' at source token span [8,9).",
  "edit_validity": "acceptable_alternative",
  "rule_id": "1",
  "rule_text": "replace 'at' with 'in'",
  "evidence_spans": [
    {
      "text": "In my c
- `rf-edit-0273::qwen_small::rule_grounded`: ```json
{
  "edit_description": "Replace 'end' with 'end,' at source token span [2,3).",
  "edit_validity": "acceptable_alternative",
  "rule_id": "1",
  "rule_text": "Replace 'end' with 'end,' at source token span [2,3).",
  "evidence_span
- `rf-edit-0240::qwen_small::natural`: ```json
{
  "edit_description": "I'd like to tell you about my favorite restaurant. It's called 'Lemon'. I go there every week. It has different food than other restaurants. I'd like chicken crispy with garlic sauce. It's an excellent choic
- `rf-edit-0240::qwen_small::rule_grounded`: ```json
{
  "edit_description": "I'd like to tell you about my favorite restaurant. It's called 'Lemon'. I go there every week. It has different food than other restaurants. I'd like chicken crispy with garlic sauce. It's an excellent choic
- `rf-edit-0183::qwen_small::natural`: ```json
{
  "edit_description": "Replace 'material.' with 'material' at source token span [42,44).",
  "edit_validity": "valid",
  "rule_id": "1",
  "rule_text": "Replace 'material.' with 'material' at source token span [42,44).",
  "eviden
- `rf-edit-0278::qwen_small::rule_grounded`: ```json
{
  "edit_description": "Replace '.' with 'side.' at source token span [18,19).",
  "edit_validity": "valid",
  "rule_id": "no_change",
  "rule_text": "No change required.",
  "evidence_spans": [
    {"text": ".", "start": 18, "end"
- `rf-edit-0231::qwen_small::rule_grounded`: ```json
{
  "edit_description": "Replace 'should' with 'is to' at source token span [1,2).",
  "edit_validity": "acceptable_alternative",
  "rule_id": "1",
  "rule_text": "The goal is to develop their awareness of the public manner.",
  "ev
- `rf-edit-0081::qwen_small::natural`: ```json
{
  "edit_description": "Replace 'ever' with 'always' at source token span [2,3).",
  "edit_validity": "acceptable_alternative",
  "rule_id": "1",
  "rule_text": "Replace 'ever' with 'always'",
  "evidence_spans": [
    {
      "tex
- `rf-edit-0111::qwen_small::rule_grounded`: ```json
{
  "edit_description": "Replace 'champion' with 'championship' at source token span [7,8).",
  "edit_validity": "acceptable_alternative",
  "rule_id": "1",
  "rule_text": "replace 'champion' with 'championship'",
  "evidence_spans"
- `rf-edit-0273::qwen_small::natural`: ```json
{
  "edit_description": "Replace 'end' with 'end,' at source token span [2,3).",
  "edit_validity": "acceptable_alternative",
  "rule_id": "1",
  "rule_text": "Replace 'end' with 'end,' at source token span [2,3).",
  "evidence_span
- `rf-edit-0068::qwen_small::rule_grounded`: ```json
{
  "edit_description": "Replace 'almost' with 'most' at the source token span [10,11).",
  "edit_validity": "acceptable_alternative",
  "rule_id": "replace_almost_most",
  "rule_text": "Replace 'almost' with 'most' at the source to
- `rf-edit-0167::qwen_small::natural`: ```json
{
  "edit_description": "Replace 'example' with 'example,' at source token span [1,2).",
  "edit_validity": "valid",
  "rule_id": "1",
  "rule_text": "Replace 'example' with 'example,'",
  "evidence_spans": [
    {
      "text": "Fo
- `rf-edit-0284::qwen_small::natural`: ```json
{
  "edit_description": "Replace 'city' with 'city;' at source token span [7,8)",
  "edit_validity": "acceptable_alternative",
  "rule_id": "1",
  "rule_text": "Replace 'city' with 'city;' at source token span [7,8)",
  "evidence_sp
- `rf-edit-0074::qwen_small::natural`: ```json
{
  "edit_description": "Insert 'are' at the source token span [37,37).",
  "edit_validity": "valid",
  "rule_id": "12345",
  "rule_text": "Insert 'are' at the source token span [37,37).'",
  "evidence_spans": [
    {
      "text": 
- `rf-edit-0289::qwen_small::natural`: ```json
{
  "edit_description": "Replace 'finally' with 'finally' at source token span [10,11).",
  "edit_validity": "valid",
  "rule_id": "1001",
  "rule_text": "Replace 'finally' with 'finally' at source token span [10,11).",
  "evidence_
- `rf-edit-0009::qwen_small::rule_grounded`: ```json
{
  "edit_description": "Replace 'try' with 'tries' at source token span [3,4).",
  "edit_validity": "acceptable_alternative",
  "rule_id": "rule_grounded",
  "rule_text": "replace 'try' with 'tries'",
  "evidence_spans": [
    {"te
- `rf-edit-0033::qwen_small::rule_grounded`: ```json
{
  "edit_description": "Delete 'the' at source token span [34,35)",
  "edit_validity": "acceptable_alternative",
  "rule_id": "1",
  "rule_text": "The edit deletes the word 'the' at the specified source token span.",
  "evidence_sp
- `rf-edit-0141::qwen_small::natural`: ```json
{
  "edit_description": "Replace 'nocive' with 'harmful' at source token span [5,6).",
  "edit_validity": "acceptable_alternative",
  "rule_id": "1",
  "rule_text": "Replace 'nocive' with 'harmful' at source token span [5,6).",
  "e

## Interpretation

These teacher candidates are model-generated explanations for verifier filtering and failure analysis. They are not human gold and should not be used as positives without RuleFaith validation.
