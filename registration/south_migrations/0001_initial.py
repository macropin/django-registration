# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RegistrationProfile'
        db.create_table(u'registration_registrationprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['user.User'], unique=True)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'registration', ['RegistrationProfile'])


    def backwards(self, orm):
        # Deleting model 'RegistrationProfile'
        db.delete_table(u'registration_registrationprofile')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.accommodation': {
            'Meta': {'object_name': 'Accommodation'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_complement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.City']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'the_geom': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AccommodationType']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'core.accommodationtype': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'AccommodationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.attraction': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'Attraction'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'the_geom': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AttractionType']"})
        },
        u'core.attractiontype': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'AttractionType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.city': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'og_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'og_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'og_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'the_geom': ('django.contrib.gis.db.models.fields.PointField', [], {})
        },
        u'core.feeding': {
            'Meta': {'object_name': 'Feeding'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_complement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.City']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'the_geom': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.FeedingType']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'core.feedingtype': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'FeedingType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.roadmap': {
            'Meta': {'ordering': "(u'-modified',)", 'object_name': 'Roadmap'},
            'cities': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.City']", 'symmetrical': 'False', 'through': u"orm['core.RoadmapCity']", 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'og_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'og_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'og_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.User']"})
        },
        u'core.roadmapcity': {
            'Meta': {'unique_together': "((u'roadmap', u'city'),)", 'object_name': 'RoadmapCity'},
            'accommodations': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Accommodation']", 'symmetrical': 'False', 'through': u"orm['core.RoadmapCityAccommodation']", 'blank': 'True'}),
            'attractions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Attraction']", 'symmetrical': 'False', 'through': u"orm['core.RoadmapCityAttraction']", 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.City']"}),
            'feedings': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Feeding']", 'symmetrical': 'False', 'through': u"orm['core.RoadmapCityFeeding']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roadmap': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Roadmap']"})
        },
        u'core.roadmapcityaccommodation': {
            'Meta': {'unique_together': "((u'roadmapcity', u'accommodation'),)", 'object_name': 'RoadmapCityAccommodation'},
            'accommodation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Accommodation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roadmapcity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.RoadmapCity']"})
        },
        u'core.roadmapcityattraction': {
            'Meta': {'unique_together': "((u'roadmapcity', u'attraction'),)", 'object_name': 'RoadmapCityAttraction'},
            'attraction': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Attraction']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roadmapcity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.RoadmapCity']"})
        },
        u'core.roadmapcityfeeding': {
            'Meta': {'unique_together': "((u'roadmapcity', u'feeding'),)", 'object_name': 'RoadmapCityFeeding', 'db_table': "u'roadmap_city_feeding'"},
            'feeding': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Feeding']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roadmapcity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.RoadmapCity']"})
        },
        u'registration.registrationprofile': {
            'Meta': {'object_name': 'RegistrationProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['user.User']", 'unique': 'True'})
        },
        u'user.user': {
            'Meta': {'ordering': "(u'name', u'email')", 'unique_together': "((u'email',),)", 'object_name': 'User'},
            'access_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'favorites_roadmaps': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'sgusers_favorited'", 'symmetrical': 'False', 'to': u"orm['core.Roadmap']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'sguser_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_access': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'photo_dir': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'sguser_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        }
    }

    complete_apps = ['registration']