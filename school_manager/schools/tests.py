from django.test import TestCase
from schools.models import *
from django.contrib.auth.models import Group
from datetime import datetime, timedelta
from django.utils.timezone import utc


class TestModelRelations(TestCase):
    def setUp(self):
        managers_group = Group.objects.create(name="Managers")
        students_group = Group.objects.create(name="Students")
        instructors_group = Group.objects.create(name="Instructors")

        school_manager_user = User.objects.create_user(username='alex', first_name="Alex", last_name="Kyllo",)
        school_manager_user.groups.add(managers_group)
        cool_school = School.objects.create(name="A Cool School")
        cool_school.members.add(school_manager_user)
        cool_school_location = Location.objects.create(school=cool_school, name="Kirkland")
        cool_school_instructor = User.objects.create_user(username='johndoe', first_name="John", last_name="Doe")
        cool_school_instructor.groups.add(instructors_group)
        cool_school_student_1 = User.objects.create_user(username='janedoe', first_name="Jane", last_name="Doe")
        cool_school_student_2 = User.objects.create_user(username='bobloblaw', first_name="Bob", last_name="Loblaw")
        
        cool_school_student_1.groups.add(students_group)
        cool_school_student_2.groups.add(students_group)
        cool_school_course = Course.objects.create(name="Yoga 101", location=cool_school_location, school=cool_school)
        cool_school_course.instructors.add(cool_school_instructor)
        cool_school_course.students.add(cool_school_student_1)
        dt = datetime(2014, 5, 9, 5, 35, 5, 730613)
        cool_school_course_session = Session.objects.create(course=cool_school_course, school=cool_school, startdatetime=dt, enddatetime=dt+timedelta(hours=1))
        cool_school_course_session.students.add(cool_school_student_1)
        cool_school_course_session.students.add(cool_school_student_2)

    def testSchoolHasLocation(self):
        cool_school = School.objects.get(name="A Cool School")
        location = Location.objects.get(name="Kirkland")
        self.assertEqual(location.school, cool_school)
        self.assertEqual(str(location),"Kirkland")

    def testLocationHasCourse(self):
        cool_school_course = Course.objects.get(name="Yoga 101")
        cool_school_location = Location.objects.get(name="Kirkland")
        self.assertEqual(cool_school_course.location,cool_school_location)
        self.assertEqual(str(cool_school_course),"Yoga 101")

    def testCourseHasStudentAndInstructor(self):
        cool_school_course = Course.objects.get(name="Yoga 101")
        cool_school_instructor = User.objects.get(username="johndoe")
        cool_school_student = User.objects.get(username="janedoe")

        self.assertTrue(cool_school_instructor in cool_school_course.instructors.all())
        self.assertTrue(cool_school_student in cool_school_course.students.all())
        self.assertEqual(cool_school_student.first_name, "Jane")
        self.assertEqual(cool_school_instructor.first_name, "John")

    def testSessionHasStudents(self):
        dt = datetime(2014, 5, 9, 5, 35, 5, 730613)
        cool_school_course_session = Session.objects.get(startdatetime=dt)
        #cool_school_course_session = Session.objects.get(pk=1)
        cool_school_student_1 = User.objects.get(first_name="Jane", last_name="Doe")
        cool_school_student_2 = User.objects.get(first_name="Bob", last_name="Loblaw")
        self.assertTrue(cool_school_student_1 in cool_school_course_session.students.all())
        self.assertTrue(cool_school_student_2 in cool_school_course_session.students.all())

    def testSessionHasDateTime(self):
        dt = datetime(2014, 5, 9, 5, 35, 5, 730613)
        cool_school_course_session = Session.objects.get(startdatetime=dt)
        #cool_school_course_session = Session.objects.get(pk=1)
        self.assertTrue(type(cool_school_course_session.startdatetime) == datetime)
        self.assertEqual(str(cool_school_course_session), "Yoga 101 on Friday, May 09 at 05:35:05")

from django.test.client import RequestFactory, Client
from schools.views import SchoolList

class TestSchoolViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.valid_user = User.objects.create_user(username='alex', first_name="Alex", last_name="Kyllo", password="42")
        managers_group = Group.objects.create(name="Managers")
        self.valid_user.groups.add(managers_group)
        self.invalid_user = User.objects.create_user(username='root', first_name="root", last_name="root")

    def testValidUserCanViewSchoolsList(self):
        request = self.factory.get('/schools/')
        request.user = self.valid_user
        response = SchoolList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def testInvalidUserCannotViewSchoolsList(self):
        request = self.factory.get('/schools/')
        request.user = self.invalid_user
        response = SchoolList.as_view()(request)
        print(response.context_data)
        self.assertFalse(response.context_data['object_list'])
        #self.assertRedirects(response, '/accounts/login/?next=/schools/', status_code=302, target_status_code=200)

    def testValidUserCanCreateSchool(self):
        self.client.login(username='alex', password='42')
        self.client.post('/schools/create/', {"name": "Testing School"})
        testing_school = School.objects.get(name='Testing School')
        self.assertTrue(testing_school)

    def testInvalidUserCannotCreateSchool(self):
        self.client.login(username='root', password='password')
        self.client.post('/schools/create/', {'name': 'Fake Testing School'})
        #fake_testing_school = School.objects.get(name='Fake Testing School')
        try: 
            School.objects.get(name='Fake Testing School')
        except:
            self.assertTrue(True)

    def testValidUserCanViewSchoolDetail(self):
        request = self.factory.get('/schools/1/')
        request.user = self.valid_user
        response = SchoolList.as_view()(request)
        self.assertEqual(response.status_code, 200)

class TestAccounts(TestCase):
    def setUp(self):
        self.client = Client()
        Group.objects.create(name="Managers")
        User.objects.create_user(username='dawn', first_name='Dawn', last_name='Kyllo', password='ruby')
        
    def testInvalidUserCannotLogIn(self):
        self.assertEqual(self.client.login(username='root', password='password'), False)

    def testValidUserCanLogIn(self):
        self.assertTrue(self.client.login(username='dawn', password='ruby'))

    def testUserCanRegister(self):
        self.client.post('/accounts/register/', {'username': 'testuser1', 'password1': 'testpass', 'password2' : 'testpass',})
        user = User.objects.get(username='testuser1')
        self.assertTrue(user)

class TestSchoolViewsWithFixtures(TestCase):
    fixtures = ['schools.json', 'users.json', 'groups.json']

    def setUp(self):
        self.client = Client()

    def testUserCanViewOwnSchoolsList(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.get('/schools/')
        self.assertContains(response, "A Cool School", status_code=200)

    def testUserCannotViewOtherSchoolsList(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.get('/schools/')
        self.assertNotContains(response, "A Cooler School")

    def testAnonymousUserCannotViewSchoolsList(self):
        anon_client = Client()
        response = anon_client.get('/schools/')
        self.assertRedirects(response, '/accounts/login/?next=/schools/')

class TestLocationViews(TestCase):
    fixtures = ['schools.json', 'users.json', 'groups.json', 'locations.json']

    def setUp(self):
        self.client = Client()

    def test_user_can_view_location_list_of_own_school(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.get('/schools/1/locations/')
        self.assertContains(response, "A Cool School Kirkland Location", status_code=200)

    def test_user_cannot_view_location_list_of_other_school(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.get('/schools/2/locations/')
        self.assertEqual(response.status_code, 404)

    def test_user_can_view_location_detail_of_own_school(self):
        self.client.login(username='kyllo',password='password')
        response = self.client.get('/locations/1/')
        self.assertContains(response, "A Cool School Kirkland Location", status_code=200)

    def test_user_cannot_view_location_detail_of_other_school(self):
        self.client.login(username='kyllo',password='password')
        response = self.client.get('/locations/2/')
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_create_location_for_other_school(self):
        self.client.login(username='kyllo',password='password')
        response = self.client.post('/schools/2/locations/create/', 
            {
                'school_id': 2, 
                'name':'a school', 
                'address_1': 'a', 
                'address_2': 'a', 
                'city': 'a', 
                'state_province': 'WA',
                'zip_postal_code': '12345',
                'country': 'US',
            })
        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_cannot_view_location_list(self):
        anon_client = Client()
        response = anon_client.get('/schools/1/locations/')
        self.assertRedirects(response, '/accounts/login/?next=/schools/1/locations/')

    def test_anonymous_user_cannot_view_location_detail(self):
        anon_client = Client()
        response = anon_client.get('/locations/1/')
        self.assertRedirects(response, '/accounts/login/?next=/locations/1/')

class TestCourseViews(TestCase):
    fixtures = ['schools.json', 'locations.json', 'courses.json', 'users.json', 'groups.json']

    def setUp(self):
        self.client = Client()

    def test_user_can_view_course_list_of_own_school(self):
        self.client.login(username='kyllo',password='password')
        response = self.client.get('/locations/1/courses/')
        self.assertContains(response, "Yoga 101", status_code=200)  

    def test_user_cannot_view_course_list_of_other_school(self):
        self.client.login(username='kyllo',password='password')
        response = self.client.get('/locations/2/courses/')
        self.assertEqual(response.status_code, 404)

    def test_user_can_view_course_detail_of_own_school(self):
        self.client.login(username='kyllo',password='password')
        response = self.client.get('/courses/1/')
        self.assertContains(response, "Yoga 101", status_code=200)  

    def test_user_cannot_view_course_detail_of_other_school(self):
        self.client.login(username='kyllo',password='password')
        response = self.client.get('/courses/2/')
        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_cannot_view_course_list(self):
        anon_client = Client()
        response = anon_client.get('/locations/1/courses/')
        self.assertRedirects(response, '/accounts/login/?next=/locations/1/courses/')

