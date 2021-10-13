from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.http import HttpResponse

from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import json
from datetime import date
import os
import pygame
import numpy
import cv2

from account.views import is_auth, StatsBaseView, PageManager, remove_urls_nodes


class SetCustomThemeView(StatsBaseView):
    def add_color(self, request, name):
        default_value = None
        color = request.POST.get(name)
        color = default_value if (color is None) else color
        #print('color-' + name + ': ', color)
        return color

    def post(self, request, *args, **kwargs):
        path = remove_urls_nodes(request.get_full_path(), 1)
        response = redirect(path)

        colors = dict()
        colors['nav_color'] = self.add_color(request, "theme-maxsize__left-nav")
        colors['nav_icons_color'] = self.add_color(request, "theme-maxsize__left-nav__icons")
        colors['nav_hover_color'] = self.add_color(request, "theme-maxsize__left-nav__hover")
        colors['active_page_color'] = self.add_color(request, "theme-maxsize__left-nav__active-page")
        colors['header_color'] = self.add_color(request, "theme-maxsize__header")
        colors['header_icons_color'] = self.add_color(request, "theme-maxsize__header__icons")
        colors['content_color'] = self.add_color(request, "theme-maxsize__body")
        colors['blocks_color'] = self.add_color(request, "theme-maxsize__body__content")
        colors['main_text_color'] = self.add_color(request, "theme-maxsize__text-color")
        colors['main_invert_text_color'] = self.add_color(request, "theme-maxsize__text-invert-color")
        colors['homework_done_color'] = self.add_color(request, "theme-maxsize__homework-done")
        colors['homework_expected_color'] = self.add_color(request, "theme-maxsize__homework-expected")
        colors['homework_not_done_color'] = self.add_color(request, "theme-maxsize__homework-not-done")

        max_age = 365 * 24 * 60 * 60
        response.set_cookie('custom_theme', json.dumps(colors), max_age=max_age)

        return response

class SetThemeView(StatsBaseView):
    def post(self, request, *args, **kwargs):
        theme = request.POST.get("theme")

        if theme is None:
            theme = 'light'

        path = remove_urls_nodes(request.get_full_path(), 1)
        response = redirect(path)

        theme_cookie_age = 365 * 24 * 60 * 60
        response.set_cookie('theme', theme, max_age=theme_cookie_age)

        return response



def parse_int(arr):
    for i in range(len(arr)):
        try:
            arr[i] = int(arr[i])
        except:
            arr[i] = None

    return arr

class PillowMixin(object):
    def pillow(self, image, position1, position2, canvas_size):
        pillow_image = Image.open(image)

        if position1[0] == None or position1[1] == None or position2[0] == None or position2[1] == None or canvas_size[0] == None or canvas_size[1] == None:
            position1 = [0, 0]
            position2 = pillow_image.size

        else:
            one_percent_w = canvas_size[0]/100
            position1[0] = (position1[0] / one_percent_w * pillow_image.size[0] / 100)
            position2[0] = (position2[0] / one_percent_w * pillow_image.size[0] / 100)

            one_percent_h = canvas_size[1]/100
            position1[1] = (position1[1] / one_percent_h * pillow_image.size[1] / 100)
            position2[1] = (position2[1] / one_percent_h * pillow_image.size[1] / 100)

        new_img = pillow_image.crop((position1[0], position1[1], position2[0], position2[1]))

        buffer = BytesIO()
        new_img.save(fp=buffer, format='PNG')
        buff_val = buffer.getvalue()
        return ContentFile(buff_val)

    def draw_converted_image(self):
        self.surface.fill('black')
        char_indices = self.cv2_image // self.ASCII_COEFF
        for x in range(0, self.image_w, self.CHAR_STEP):
            for y in range(0, self.image_h, self.CHAR_STEP):
                char_index = char_indices[x, y]
                if char_index:
                    self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], (x, y))
        pygame.display.flip()

    def save_image(self):
        pygame_image = pygame.surfarray.array3d(self.surface)
        transposed_image = cv2.transpose(pygame_image)
        pillow_image = Image.fromarray(transposed_image)

        buffer = BytesIO()
        pillow_image.save(fp=buffer, format='PNG')
        buff_val = buffer.getvalue()
        return ContentFile(buff_val)

    def get_image(self, image):
        pil_image = Image.open(image)
        cv2_image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
        transposed_image = cv2.transpose(cv2_image)
        gray_image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2GRAY)
        return gray_image

    def hack_img(self, image):
        self.cv2_image = self.get_image(image)
        self.img_size = self.image_w, self.image_h = self.cv2_image.shape[0], self.cv2_image.shape[1]
        print(self.img_size)

        pygame.init()
        self.surface = pygame.display.set_mode(self.img_size)
        self.font_size = 12
        self.font = pygame.font.SysFont('Сourier', self.font_size, bold=True)

        self.ASCII_CHARS = ' .",:;!~+-xmo*#W&8@'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)

        self.CHAR_STEP = int(self.font_size * 0.6)
        self.RENDERED_ASCII_CHARS = [self.font.render(char, False, 'green') for char in self.ASCII_CHARS]

        self.draw_converted_image()
        #self.save_image()
        result_file = self.save_image()
        pygame.quit()
        return result_file






class ProfileView(StatsBaseView, PageManager, PillowMixin):
    template_name = "profile/index.html"
    active_page = 3

    def post(self, request, *args, **kwargs):
        user = auth.get_user(request)  # request.user

        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        dob = request.POST.get("dob", "")
        full_name = request.POST.get("full_name", "")

        if 'self_img' in request.FILES:
            user.self_img = request.FILES['self_img']
            pos1 = [0, 0]
            pos2 = [0, 0]
            canvas_size = [0, 0]
            pos1[0] = request.POST.get("x1", None)
            pos1[1] = request.POST.get("y1", None)
            pos2[0] = request.POST.get("x2", None)
            pos2[1] = request.POST.get("y2", None)
            canvas_size[0] = request.POST.get("canvas_w", None)
            canvas_size[1] = request.POST.get("canvas_h", None)

            pos1 = parse_int(pos1)
            pos2 = parse_int(pos2)
            canvas_size = parse_int(canvas_size)

            if pos1 == pos2:
                pillow_image = self.hack_img(user.self_img)
            else:
                pillow_image = self.pillow(user.self_img, pos1, pos2, canvas_size)
            image_file = InMemoryUploadedFile(pillow_image, None, str(user)+'_img.png', 'image/png', pillow_image.tell, None)
            request.FILES['self_img'] = image_file  # rewrite img in POST for success form validation
            user.self_img = request.FILES['self_img']


        if user.username != username and username != '':
            user.username = username

        if user.email != email and email != '':
            user.email = email

        if user.full_name != full_name and full_name != '':
            user.full_name = full_name

        if user.dob != dob and dob != '':
            #print('dob', user.dob, dob)
            user.dob = dob

        user.save()
        request.user = user
        '''
        print(request.user)
        print('username', user.username)
        print('email', user.email)
        print('full_name', user.full_name)
        print('dob', user.dob)
        print('self_img', user.self_img)
        '''
        context = self.get_context_data()
        return self.render_to_response(context)



class BasePasswordChangeDoneView(PasswordChangeDoneView, StatsBaseView):
    template_name='profile/change_password_done.html'

    def get_context_data(self, **kwargs):
        print()
        print(self.get_success_url())
        stats_context = StatsBaseView.get_context_data(self, **kwargs)
        context = super(PasswordChangeDoneView, self).get_context_data(**kwargs)
        context.update(stats_context)
        print(context)
        return context

class BasePasswordChangeView(PasswordChangeView, StatsBaseView):
    template_name='profile/change_password.html'

    def get_context_data(self, **kwargs):
        print()
        print(self.get_success_url())
        stats_context = StatsBaseView.get_context_data(self, **kwargs)
        context = super(PasswordChangeView, self).get_context_data(**kwargs)
        context.update(stats_context)
        print(context)
        return context
