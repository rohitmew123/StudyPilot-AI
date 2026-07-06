# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from app.agent import (
    generate_daily_study_plan,
    generate_revision_plan,
    generate_interview_prep_questions
)


def test_generate_daily_study_plan():
    res = generate_daily_study_plan(6, ["Maths", "Science"], "Learn calculus")
    assert "Daily Study Plan" in res
    assert "Maths" in res
    assert "Science" in res


def test_generate_revision_plan():
    res = generate_revision_plan(["SQL", "Git"], 3)
    assert "Revision Plan" in res
    assert "SQL" in res


def test_generate_interview_prep_questions():
    res = generate_interview_prep_questions("Software Engineer", ["System Design"])
    assert "Software Engineer" in res
    assert "System Design" in res

